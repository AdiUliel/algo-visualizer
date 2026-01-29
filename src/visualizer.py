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
WEIGHT_COLOR = (200, 0, 0)
HIGHLIGHT_TEXT = (0, 102, 204)

def draw_edge(screen, edge, font, show_weights=True):
    pygame.draw.line(screen, EDGE_COLOR, (edge.start.x, edge.start.y), (edge.end.x, edge.end.y), EDGE_WIDTH)
    if show_weights:
        mid_x = (edge.start.x + edge.end.x) / 2
        mid_y = (edge.start.y + edge.end.y) / 2
        weight_surf = font.render(str(edge.weight), True, WEIGHT_COLOR)
        screen.blit(weight_surf, (mid_x + 8, mid_y - 12))

def draw_node(screen, node, font, is_unreachable=False):
    base = COLORS.get(node.state, COLORS["unvisited"])
    color = node.tint if node.tint is not None else base
    pygame.draw.circle(screen, color, (node.x, node.y), RADIUS)
    pygame.draw.circle(screen, OUTLINE_COLOR, (node.x, node.y), RADIUS, 2)
    
    label = font.render(str(node.id), True, TEXT_COLOR)
    rect = label.get_rect(center=(node.x, node.y))
    screen.blit(label, rect)
    
    if is_unreachable:
        inf_surf = font.render("∞", True, (200, 0, 0))
        screen.blit(inf_surf, (node.x + 12, node.y - 25))

def draw_sidebar(screen, graph, font):
    panel_w, pad = 220, 10
    x0 = screen.get_width() - panel_w
    pygame.draw.rect(screen, (235, 235, 235), (x0, 0, panel_w, screen.get_height()))
    
    mode = graph.fx.get("mode", "Ready")
    mode_surf = font.render(f"MODE: {mode}", True, HIGHLIGHT_TEXT)
    screen.blit(mode_surf, (x0 + pad, 10))

    data_title = "Queue/PQ:" if "queue" in graph.fx else ("Stack:" if "stack" in graph.fx else "")
    if data_title:
        screen.blit(font.render(data_title, True, (40, 40, 40)), (x0 + pad, 40))
        items = graph.fx.get("queue", graph.fx.get("stack", []))
        y = 60
        for item in items[:12]:
            screen.blit(font.render(str(item), True, (60, 60, 60)), (x0 + pad, y))
            y += 18

    log = graph.fx.get("log", [])
    if log:
        ly = 320
        screen.blit(font.render("Visit Log:", True, (40, 40, 40)), (x0 + pad, ly))
        y_offset = ly + 22
        for entry in log[-15:]:
            log_surf = font.render(f"• {entry}", True, (100, 100, 100))
            screen.blit(log_surf, (x0 + pad, y_offset))
            y_offset += 18

def draw_graph(screen, graph, font):
    mode = graph.fx.get("mode", "Ready")
    is_dijkstra = "DIJKSTRA" in mode.upper()
    is_ready = mode == "Ready"
    show_weights = is_dijkstra or is_ready
    unreachable_nodes = graph.fx.get("unreachable", [])

    for e in graph.edges:
        draw_edge(screen, e, font, show_weights)
    for node in graph.nodes.values():
        draw_node(screen, node, font, is_unreachable=(node.id in unreachable_nodes))
    
    if "cursor" in graph.fx:
        x, y = graph.fx["cursor"]
        pygame.draw.circle(screen, (50, 120, 255), (int(x), int(y)), 6)
    
    draw_sidebar(screen, graph, font)