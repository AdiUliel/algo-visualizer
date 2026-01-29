import heapq
from .animation_helpers import animate, ease_out_cubic, lerp

def dijkstra_steps(graph, start_id):
    start = graph.nodes[start_id]
    distances = {node_id: float('inf') for node_id in graph.nodes}
    distances[start_id] = 0
    pq = [(0, start_id)]
    
    while pq:
        curr_dist, u_id = heapq.heappop(pq)
        u = graph.nodes[u_id]
        if u.state == "visited": continue
            
        graph.fx["log"].append(f"{u.id}(d:{curr_dist})")
        u.state = "visiting"
        yield from animate(graph, 0.70, lambda p: None) 

        for v in u.neighbors:
            weight = graph.get_edge_weight(u.id, v.id)
            new_dist = curr_dist + weight
            
            graph.fx["cursor"] = (u.x, u.y)
            yield from animate(graph, 0.60, lambda p: graph.fx.update({"cursor": (lerp(u.x, v.x, ease_out_cubic(p)), lerp(u.y, v.y, ease_out_cubic(p)))}))
            graph.fx.pop("cursor", None)

            if new_dist < distances[v.id]:
                distances[v.id] = new_dist
                v.parent = u
                heapq.heappush(pq, (new_dist, v.id))
                graph.fx["queue"] = [f"ID:{id}|D:{d}" for d, id in pq]
                yield from animate(graph, 0.40, lambda p: None)

        u.state = "visited"
        yield

    graph.fx["unreachable"] = [n.id for n in graph.nodes.values() if n.state == "unvisited"]
    yield