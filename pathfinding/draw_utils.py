import pygame
from. constants import *

def draw_grid(grid, window):
    window.fill(COLORS["WHITE"])
    for row in grid:
        for cell in row:
            cell.draw_cell(window)

    # Draw grid lines
    for col in range(len(grid[0])):
        pygame.draw.line(window, COLORS["GREY"], (col * cell.width, 0), (col * cell.width, len(grid) * cell.height))
    for row in range(len(grid)):
        pygame.draw.line(window, COLORS["GREY"], (0, row * cell.height), (len(grid[0]) * cell.width, row * cell.height))

    pygame.display.update()
