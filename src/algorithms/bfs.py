from collections import deque
from .animation_helpers import animate, ease_out_cubic, lerp, lerp_color


def bfs_steps(graph, start_id):
    graph.reset_states()
    start = graph.nodes[start_id]

    q = deque([start])
    graph.fx["queue"] = [start.id]

    start.state = "visiting"
    start_base = (180,180,180)
    amber = (255,215,0)
    def tint_start(p):
        start.tint = lerp_color(start_base, amber, ease_out_cubic(p))
    yield from animate(graph, 0.20, tint_start)
    start.tint = None
    yield

    while q:
        u = q.popleft()
        graph.fx["queue"] = [n.id for n in q]

        for v in u.neighbors:
            if v.state == "unvisited":
                graph.fx["cursor"] = (u.x, u.y)
                ux, uy, vx, vy = u.x, u.y, v.x, v.y
                def move(p):
                    p2 = ease_out_cubic(p)
                    graph.fx["cursor"] = (lerp(ux, vx, p2), lerp(uy, vy, p2))
                yield from animate(graph, 0.30, move)
                graph.fx.pop("cursor", None)

                v.state = "visiting"
                def tint_v(p):
                    v.tint = lerp_color((180,180,180), amber, ease_out_cubic(p))
                yield from animate(graph, 0.15, tint_v)
                v.tint = None

                v.parent = u
                q.append(v)
                graph.fx["queue"] = [n.id for n in q]
                yield

        green = (120,200,120)
        def finish_u(p):
            u.tint = lerp_color(amber, green, ease_out_cubic(p))
        yield from animate(graph, 0.20, finish_u)
        u.state = "visited"
        u.tint = None
        yield
