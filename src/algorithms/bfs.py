from collections import deque
from .animation_helpers import animate, ease_out_cubic, lerp

def bfs_steps(graph, start_id):
    all_nodes = list(graph.nodes.values())
    if start_id in graph.nodes:
        start_node = graph.nodes[start_id]
        all_nodes.remove(start_node)
        all_nodes.insert(0, start_node)

    for root_node in all_nodes:
        if root_node.state != "unvisited": continue

        q = deque([root_node])
        graph.fx["queue"] = [root_node.id]
        root_node.state = "visiting"
        yield from animate(graph, 0.60, lambda p: None) 
        
        while q:
            u = q.popleft()
            graph.fx["log"].append(u.id)
            graph.fx["queue"] = [n.id for n in q]

            for v in u.neighbors:
                if v.state == "unvisited":
                    graph.fx["cursor"] = (u.x, u.y)
                    ux, uy, vx, vy = u.x, u.y, v.x, v.y
                    yield from animate(graph, 0.80, lambda p: graph.fx.update({"cursor": (lerp(ux, vx, ease_out_cubic(p)), lerp(uy, vy, ease_out_cubic(p)))}))
                    graph.fx.pop("cursor", None)

                    v.state = "visiting"
                    v.parent = u
                    q.append(v)
                    graph.fx["queue"] = [n.id for n in q]
                    yield

            u.state = "visited"
            yield from animate(graph, 0.40, lambda p: None)