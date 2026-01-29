from .animation_helpers import animate, ease_out_cubic, lerp, lerp_color

def dfs_steps(graph, start_id):
    all_nodes = list(graph.nodes.values())
    if start_id in graph.nodes:
        start_node = graph.nodes[start_id]
        all_nodes.remove(start_node)
        all_nodes.insert(0, start_node)

    amber = (255, 215, 0); green = (120, 200, 120)

    for root_node in all_nodes:
        if root_node.state != "unvisited":
            continue

        stack = [(root_node, 0)]
        root_node.state = "visiting"
        graph.fx["log"].append(f"Start Component: {root_node.id}")
        
        yield from animate(graph, 0.70, lambda p: None)

        while stack:
            node, i = stack[-1]
            graph.fx["stack"] = [n.id for (n, _) in stack]

            if i < len(node.neighbors):
                nxt = node.neighbors[i]
                stack[-1] = (node, i + 1)

                if nxt.state == "unvisited":
                    graph.fx["cursor"] = (node.x, node.y)
                    yield from animate(graph, 0.80, lambda p: graph.fx.update({
                        "cursor": (lerp(node.x, nxt.x, ease_out_cubic(p)), 
                                   lerp(node.y, nxt.y, ease_out_cubic(p)))
                    }))
                    graph.fx.pop("cursor", None)

                    nxt.parent = node
                    nxt.state = "visiting"
                    graph.fx["log"].append(nxt.id)
                    stack.append((nxt, 0))
                    yield
            else:
                u, _ = stack.pop()
                yield from animate(graph, 0.40, lambda p: None)
                u.state = "visited"
                graph.fx["stack"] = [n.id for (n, _) in stack]
                yield