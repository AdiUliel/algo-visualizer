import sys
import pygame
import tkinter as tk
from tkinter import simpledialog, messagebox

from src.infrastructure.graph import Graph, build_demo_graph
from src.visualizer import draw_graph
from src.algorithms.bfs import bfs_steps
from src.algorithms.dfs import dfs_steps
from src.algorithms.dijkstra import dijkstra_steps

def get_node_at_pos(graph, pos):
    for node in graph.nodes.values():
        dist = ((node.x - pos[0])**2 + (node.y - pos[1])**2)**0.5
        if dist < 20: return node
    return None

def get_edge_at_pos(graph, pos):
    for edge in graph.edges:
        x1, y1 = edge.start.x, edge.start.y
        x2, y2 = edge.end.x, edge.end.y
        px, py = pos
        line_len_sq = (x2 - x1)**2 + (y2 - y1)**2
        if line_len_sq == 0: continue
        t = max(0, min(1, ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / line_len_sq))
        proj_x = x1 + t * (x2 - x1)
        proj_y = y1 + t * (y2 - y1)
        if ((px - proj_x)**2 + (py - proj_y)**2)**0.5 < 10: return edge
    return None

def run_visualizer(algorithm: str = None, start_id: int = 1, auto_play_start: bool = False, graph: Graph | None = None):
    pygame.init()
    WIDTH, HEIGHT = 900, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Algorithm Visualizer - Editor Mode")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18, bold=True)
    help_font = pygame.font.SysFont("Consolas", 14) 
    sidebar_font = pygame.font.SysFont("Segoe UI", 17)

    last_click_time = 0
    DOUBLE_CLICK_THRESHOLD = 300 
    
    g = graph if graph is not None else build_demo_graph()
    
    if graph is None:
        for node in g.nodes.values():
            node.x += 50
            node.y += 100

    if not hasattr(g, 'fx'): g.fx = {}
    g.speed_factor = 1.0
    
    stepper = None
    auto_play = auto_play_start
    selected_node = None

    def draw_help(screen, help_font):
        lines = [
            "ALGO: BFS (B) | DFS (D) | Dijkstra (K)",
            "SYSTEM: Step (SPACE) | Autoplay (P) | Stop (O) | Clear Board (C) | Quit (ESC/Q)",
            "EDIT: L-Click (Add) | R-Click (Connect) | Double R-Click (Weight) | DEL (Delete)"
        ]
        y = 10
        for line in lines:
            surf = help_font.render(line, True, (40, 40, 40))
            screen.blit(surf, (15, y))
            y += 20

    def start_algo(algo_type, sid):
        if sid not in g.nodes: return
        nonlocal stepper, auto_play
        g.reset_states()
        g.fx["log"] = []
        if algo_type == "bfs": stepper = bfs_steps(g, sid)
        elif algo_type == "dfs": stepper = dfs_steps(g, sid)
        elif algo_type == "dijkstra": stepper = dijkstra_steps(g, sid)
        g.fx["mode"] = algo_type.upper()
        auto_play = False

    def confirm_exit():
        root = tk.Tk(); root.withdraw()
        res = messagebox.askyesno("Exit", "Are you sure you want to quit?")
        root.destroy()
        return res

    def confirm_clear():
        root = tk.Tk(); root.withdraw()
        res = messagebox.askyesno("Clear Board", "This action will delete all nodes and edges, do you wish to continue?")
        root.destroy()
        return res

    g.fx["mode"] = "Ready"
    g.fx["log"] = []

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        is_running = stepper is not None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if confirm_exit(): running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_running: continue
                curr_time = pygame.time.get_ticks()
                node = get_node_at_pos(g, mouse_pos)
                edge = get_edge_at_pos(g, mouse_pos)
                
                if event.button == 1: 
                    if not node and mouse_pos[0] < WIDTH - 180 and mouse_pos[1] > 80:
                        new_id = max(g.nodes.keys(), default=0) + 1
                        g.add_node(new_id, mouse_pos[0], mouse_pos[1])
                elif event.button == 3: 
                    if curr_time - last_click_time < DOUBLE_CLICK_THRESHOLD and edge:
                        root = tk.Tk(); root.withdraw()
                        new_w = simpledialog.askinteger("Weight", "New weight:", initialvalue=edge.weight)
                        root.destroy()
                        if new_w is not None: edge.weight = new_w
                    elif node:
                        if selected_node is None:
                            selected_node = node; node.tint = (100, 200, 255)
                        elif selected_node != node:
                            root = tk.Tk(); root.withdraw()
                            w = simpledialog.askinteger("Weight", "Weight:", initialvalue=1)
                            root.destroy()
                            try: g.add_edge(selected_node.id, node.id, w if w else 1)
                            except: pass
                            selected_node.tint = None; selected_node = None
                    else:
                        if selected_node: selected_node.tint = None; selected_node = None
                    last_click_time = curr_time

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    if confirm_exit(): running = False
                elif event.key in (pygame.K_DELETE, pygame.K_BACKSPACE) and not is_running:
                    n_del = get_node_at_pos(g, mouse_pos)
                    if n_del:
                        g.edges = [e for e in g.edges if e.start != n_del and e.end != n_del]
                        for n in g.nodes.values(): n.neighbors = [nb for nb in n.neighbors if nb != n_del]
                        del g.nodes[n_del.id]
                    else:
                        e_del = get_edge_at_pos(g, mouse_pos)
                        if e_del:
                            e_del.start.neighbors = [nb for nb in e_del.start.neighbors if nb != e_del.end]
                            if not g.directed: e_del.end.neighbors = [nb for nb in e_del.end.neighbors if nb != e_del.start]
                            g.edges.remove(e_del)
                elif event.key == pygame.K_b: start_algo("bfs", start_id)
                elif event.key == pygame.K_d: start_algo("dfs", start_id)
                elif event.key == pygame.K_k: start_algo("dijkstra", start_id)
                elif event.key == pygame.K_SPACE: 
                    if is_running: 
                        try: next(stepper)
                        except StopIteration:
                            m = g.fx.get("mode", ""); g.fx["mode"] = f"{m} (Done)"
                            stepper = None
                elif event.key == pygame.K_p: auto_play = not auto_play
                elif event.key == pygame.K_o:
                    g.reset_states(); g.fx["mode"] = "Ready"; g.fx["log"] = []
                    stepper = None; auto_play = False; selected_node = None
                elif event.key == pygame.K_c:
                    if not is_running:
                        if confirm_clear():
                            g.nodes = {}
                            g.edges = []
                            g.reset_states()
                            g.fx["mode"] = "Ready"
                            g.fx["log"] = []
                            stepper = None
                            selected_node = None

        if auto_play and is_running:
            try: next(stepper)
            except StopIteration:
                m = g.fx.get("mode", ""); g.fx["mode"] = f"{m} (Done)"
                stepper = None

        screen.fill((245, 245, 245))
        draw_graph(screen, g, font)
        draw_help(screen, help_font)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_visualizer()