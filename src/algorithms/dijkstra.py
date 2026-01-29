import heapq
from .animation_helpers import animate, ease_out_cubic, lerp, lerp_color

def dijkstra_steps(graph, start_id):
    start = graph.nodes[start_id]
    
    distances = {node_id: float('inf') for node_id in graph.nodes}
    distances[start_id] = 0
    
    pq = [(0, start_id)]
    graph.fx["queue"] = [f"{start_id}(0)"]
    
    amber = (255, 215, 0); green = (120, 200, 120); blue = (50, 120, 255)

    while pq:
        curr_dist, u_id = heapq.heappop(pq)
        u = graph.nodes[u_id]
        
        if u.state == "visited":
            continue
            
        graph.fx["log"].append(f"{u.id}(d:{curr_dist})")
        graph.fx["queue"] = [f"ID:{id}|D:{d}" for d, id in pq]

        u.state = "visiting"
        def highlight_u(p):
            u.tint = lerp_color((180, 180, 180), amber, ease_out_cubic(p))
        yield from animate(graph, 0.25, highlight_u)
        u.tint = None
        yield

        for v in u.neighbors:
            weight = graph.get_edge_weight(u.id, v.id)
            new_dist = curr_dist + weight
            
            graph.fx["cursor"] = (u.x, u.y)
            def move(p):
                p2 = ease_out_cubic(p)
                graph.fx["cursor"] = (lerp(u.x, v.x, p2), lerp(u.y, v.y, p2))
            yield from animate(graph, 0.20, move)
            graph.fx.pop("cursor", None)

            if new_dist < distances[v.id]:
                distances[v.id] = new_dist
                v.parent = u
                heapq.heappush(pq, (new_dist, v.id))
                
                def update_v(p):
                    v.tint = lerp_color((180, 180, 180), blue, ease_out_cubic(p))
                yield from animate(graph, 0.15, update_v)
                v.tint = None
                
                graph.fx["queue"] = [f"ID:{id}|D:{d}" for d, id in pq]
                yield

        def finish_u(p):
            u.tint = lerp_color(amber, green, ease_out_cubic(p))
        yield from animate(graph, 0.20, finish_u)
        u.state = "visited"
        u.tint = None
        yield