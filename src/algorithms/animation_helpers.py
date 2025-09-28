import pygame

def ease_out_cubic(t: float) -> float:
    """Ease-out cubic curve, t in [0,1]."""
    return 1.0 - (1.0 - t) ** 3

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation."""
    return a + (b - a) * t

def lerp_color(c1, c2, t: float):
    """Interpolate two RGB tuples."""
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))

def animate(graph, duration_sec: float, update):
    """
    Frame-by-frame animation driver.
    - duration_sec: nominal duration (scaled by graph.speed_factor)
    - update(progress): callback with progress in [0,1] each frame
    Yields once per frame; use `yield from animate(...)` inside your generators.
    """
    start = pygame.time.get_ticks()
    dur_ms = max(1, int(duration_sec * 1000))
    while True:
        now = pygame.time.get_ticks()
        elapsed = (now - start) * getattr(graph, "speed_factor", 1.0)
        p = min(1.0, elapsed / dur_ms)
        update(p)
        yield
        if p >= 1.0:
            break
