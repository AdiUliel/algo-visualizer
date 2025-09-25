import sys
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # image in memory that we can draw on
pygame.display.set_caption("Algorithm Visualizer") # window title
clock = pygame.time.Clock()

def mainWindow():
    
    running = True
    while running:
        screen.fill((255, 255, 255))  # white background
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()  # update the display to everything drawn on the screen since last frame
        clock.tick(60)  # limit to 60 FPS
        
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__": # This is to ensure that the mainWindow function is called only when this script is run directly, and not when imported as a module.
    mainWindow()
