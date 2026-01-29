import sys
import pygame

from src.infrastructure.graph import Graph, build_demo_graph
from src.visualizer import draw_graph
from src.algorithms.bfs import bfs_steps
from src.algorithms.dfs import dfs_steps
from src.algorithms.dijkstra import dijkstra_steps

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm Visualizer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
help_font = pygame.font.SysFont(None, 18)

def draw_help(screen):
    lines = [
        "B: BFS   D: DFS   K: Dijkstra",
        "SPACE: step    P: autoplay on/off",
        "R: reset       ESC/Q: quit",
    ]
    y = 8
    for line in lines:
        surf = help_font.render(line, True, (40, 40, 40))
        screen.blit(surf, (8, y))
        y += 18

def run_visualizer(algorithm: str = "bfs", start_id: int = 1, auto_play_start: bool = False, graph: Graph | None = None):
    g = graph if graph is not None else build_demo_graph()
    g.speed_factor = 0.4
    stepper = None
    auto_play = auto_play_start

    def start_bfs(sid):
        nonlocal stepper, auto_play
        g.reset_states()      
        g.fx["log"] = []      
        stepper = bfs_steps(g, sid)
        g.fx["mode"] = "BFS"  
        auto_play = False

    def start_dfs(sid):
        nonlocal stepper, auto_play
        g.reset_states()
        g.fx["log"] = []
        stepper = dfs_steps(g, sid)
        g.fx["mode"] = "DFS"
        auto_play = False

    def start_dijkstra(sid):
        nonlocal stepper, auto_play
        g.reset_states()
        g.fx["log"] = []
        stepper = dijkstra_steps(g, sid)
        g.fx["mode"] = "Dijkstra"
        auto_play = False

    def step_once():
        nonlocal stepper
        if stepper is None:
            return
        try:
            next(stepper)
        except StopIteration:
            old_mode = g.fx.get("mode", "")
            if "(Done)" not in old_mode:
                g.fx["mode"] = f"{old_mode} (Done)"
            stepper = None

    if algorithm.lower() == "bfs": start_bfs(start_id)
    elif algorithm.lower() == "dfs": start_dfs(start_id)
    elif algorithm.lower() == "dijkstra": start_dijkstra(start_id)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    start_bfs(start_id)
                elif event.key == pygame.K_d:
                    start_dfs(start_id)
                elif event.key == pygame.K_k:
                    start_dijkstra(start_id)
                elif event.key == pygame.K_SPACE:
                    step_once()
                elif event.key == pygame.K_p:
                    auto_play = not auto_play
                elif event.key == pygame.K_r:
                    g.reset_states()
                    g.fx["mode"] = "Ready"
                    stepper = None 
                    auto_play = False
                elif event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False

        if auto_play and stepper is not None:
            step_once()

        screen.fill((245, 245, 245))
        draw_graph(screen, g, font)
        draw_help(screen)
        pygame.display.flip()
        clock.tick(10 if auto_play else 60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_visualizer()