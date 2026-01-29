import sys
import pygame

from src.infrastructure.graph import Graph
from src.visualizer import draw_graph
from src.algorithms.bfs import bfs_steps
from src.algorithms.dfs import dfs_steps

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Algorithm Visualizer")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)
help_font = pygame.font.SysFont(None, 18)

def draw_help(screen):
    lines = [
        "B: start BFS   D: start DFS",
        "SPACE: step    P: autoplay on/off",
        "R: reset       ESC/Q: quit",
    ]
    y = 8
    for line in lines:
        surf = help_font.render(line, True, (40, 40, 40))
        screen.blit(surf, (8, y))
        y += 18

def run_visualizer(algorithm: str = "bfs", start_id: int = 1, auto_play_start: bool = False, graph: Graph | None = None):
    """
    Launch the Pygame visualizer.
    - algorithm: 'bfs' or 'dfs'
    - start_id:  node id to start from
    - auto_play_start: start in autoplay mode or not
    - graph: optional Graph object; if None, a small demo graph is created
    """
    g = graph if graph is not None else Graph(directed=False)
    if graph is None:
        g.add_node(1, 140, 100)
        g.add_node(2, 300, 200)
        g.add_node(3, 140, 320)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(1, 3)

    g.speed_factor = 0.4

    stepper = None
    auto_play = auto_play_start

    def start_bfs(start_id_local=1):
        nonlocal stepper, auto_play
        stepper = bfs_steps(g, start_id_local)
        auto_play = False

    def start_dfs(start_id_local=1):
        nonlocal stepper, auto_play
        stepper = dfs_steps(g, start_id_local)
        auto_play = False

    def step_once():
        nonlocal stepper
        if stepper is None:
            return
        try:
            next(stepper)
        except StopIteration:
            stepper = None

    if algorithm.lower() == "bfs":
        stepper = bfs_steps(g, start_id)
    elif algorithm.lower() == "dfs":
        stepper = dfs_steps(g, start_id)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

    # Main loop
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
                elif event.key == pygame.K_SPACE:
                    step_once()
                elif event.key == pygame.K_p:
                    auto_play = not auto_play
                elif event.key == pygame.K_r:
                    g.reset_states()
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
    run_visualizer(algorithm="bfs", start_id=1, auto_play_start=False)
