import pygame

RADIUS = 18
EDGE_WIDTH = 2

COLORS = {
    "unvisited": (180, 180, 180),
    "visiting":  (255, 215, 0),
    "visited":   (120, 200, 120),
}
EDGE_COLOR   = (60, 60, 60)
TEXT_COLOR   = (30, 30, 30)
OUTLINE_COLOR= (30, 30, 30)

def draw_edge(screen, edge):
    pygame.draw.line(screen, EDGE_COLOR,
                     (edge.start.x, edge.start.y),
                     (edge.end.x,   edge.end.y), EDGE_WIDTH)

def draw_node(screen, node, font):
    base = COLORS.get(node.state, COLORS["unvisited"])
    color = node.tint if node.tint is not None else base
    pygame.draw.circle(screen, color, (node.x, node.y), RADIUS)
    pygame.draw.circle(screen, OUTLINE_COLOR, (node.x, node.y), RADIUS, 2)
    label = font.render(str(node.id), True, TEXT_COLOR)
    rect = label.get_rect(center=(node.x, node.y))
    screen.blit(label, rect)

def draw_fx(screen, graph):
    # moving cursor along an edge
    if "cursor" in graph.fx:
        x, y = graph.fx["cursor"]
        pygame.draw.circle(screen, (50, 120, 255), (int(x), int(y)), 6)

def draw_sidebar(screen, graph, font):
    # Right side panel for queue/stack
    panel_w, pad = 180, 8
    x0 = screen.get_width() - panel_w
    pygame.draw.rect(screen, (235, 235, 235), (x0, 0, panel_w, screen.get_height()))
    title = "Queue (BFS)" if "queue" in graph.fx else ("Stack (DFS)" if "stack" in graph.fx else "")
    if title:
        t = font.render(title, True, (40,40,40))
        screen.blit(t, (x0 + pad, 8))
    items = graph.fx.get("queue", graph.fx.get("stack", []))
    y = 30
    for nid in items:
        s = font.render(str(nid), True, (60,60,60))
        screen.blit(s, (x0 + pad, y))
        y += 20

def draw_graph(screen, graph, font):
    for e in graph.edges:
        draw_edge(screen, e)
    for node in graph.nodes.values():
        draw_node(screen, node, font)
    draw_fx(screen, graph)
    draw_sidebar(screen, graph, font)
