from .animation_helpers import animate, ease_out_cubic, lerp, lerp_color

def dfs_steps(graph, start_id):
    start = graph.nodes[start_id]

    stack = [(start, 0)]
    graph.fx["stack"] = [n.id for (n, _) in stack]
    graph.fx["log"].append(start.id)

    amber = (255,215,0); green = (120,200,120)

    start.state = "visiting"
    def tint_start(p):
        start.tint = lerp_color((180,180,180), amber, ease_out_cubic(p))
    yield from animate(graph, 0.20, tint_start)
    start.tint = None
    yield

    while stack:
        node, i = stack[-1]
        graph.fx["stack"] = [n.id for (n, _) in stack]

        if i < len(node.neighbors):
            nxt = node.neighbors[i]
            stack[-1] = (node, i + 1)

            if nxt.state == "unvisited":
                graph.fx["cursor"] = (node.x, node.y)
                def move(p):
                    p2 = ease_out_cubic(p)
                    graph.fx["cursor"] = (lerp(node.x, nxt.x, p2),
                                          lerp(node.y, nxt.y, p2))
                yield from animate(graph, 0.30, move)
                graph.fx.pop("cursor", None)

                nxt.parent = node
                nxt.state = "visiting"
                graph.fx["log"].append(nxt.id)

                def tint_nxt(p):
                    nxt.tint = lerp_color((180,180,180), amber, ease_out_cubic(p))
                yield from animate(graph, 0.15, tint_nxt)
                nxt.tint = None

                stack.append((nxt, 0))
                graph.fx["stack"] = [n.id for (n, _) in stack]
                yield
        else:
            u, _ = stack.pop()
            def finish_node(p):
                u.tint = lerp_color(amber, green, ease_out_cubic(p))
            yield from animate(graph, 0.20, finish_node)
            u.state = "visited"
            u.tint = None
            graph.fx["stack"] = [n.id for (n, _) in stack]
            yield