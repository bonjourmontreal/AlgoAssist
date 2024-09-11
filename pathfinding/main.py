import pygame
from .visualizer import PathfindingVisualizer
from .constants import WINDOW_WIDTH, WINDOW_HEIGHT

def launch_visualizer(window):
    visualizer = PathfindingVisualizer(window)
    return visualizer.run()

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    launch_visualizer(window)