import pygame
import random
from .constants import *
from .grid import *

class MazeAlgorithm:
    def __init__(self, grid, window, delay=1):
        self.grid = grid
        self.window = window
        self.delay = delay

    def draw_grid(self):
        self.grid.draw_grid(self.window)
        pygame.display.update()
        pygame.time.delay(self.delay)

class RecursiveDFS(MazeAlgorithm):
    def start(self):
        # Pick a random starting point for the maze generation
        start_col = random.choice(range(1, COLS - 1, 2))
        start_row = random.choice(range(1, ROWS - 1, 2))
        self.generate_maze(start_col, start_row)

    def generate_maze(self, col, row):
        # Carve the starting point and draw the grid
        self.grid.grid[row][col].reset()
        self.draw_grid()

        # Define the directions for movement (up, down, left, right)
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)

        # Try each direction
        for direction in directions:
            next_col = col + direction[0]
            next_row = row + direction[1]

            # Ensure we stay within bounds and carve a path
            if 0 <= next_col < COLS and 0 <= next_row < ROWS:
                if self.grid.grid[next_row][next_col].is_barrier():
                    # Carve a path between the current and next cell
                    wall_col = col + direction[0] // 2
                    wall_row = row + direction[1] // 2
                    self.grid.grid[wall_row][wall_col].reset()
                    # Recursively carve the next cell
                    self.generate_maze(next_col, next_row)
                    # Draw grid after every carve
                    self.draw_grid()

class GrowingTree(MazeAlgorithm):
    def start(self):
        # Pick a random starting point for the maze generation
        start_col = random.choice(range(1, COLS, 2))
        start_row = random.choice(range(1, ROWS, 2))
        self.generate_maze(start_col, start_row)

    def generate_maze(self, col, row):
        # Initialize the starting cell and draw the grid
        start_cell = self.grid.grid[row][col]
        start_cell.reset()
        self.draw_grid()

        cells = [start_cell]

        while cells:
            current_cell = random.choice(cells)
            directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            random.shuffle(directions)

            carved_any = False
            for direction in directions:
                next_col = current_cell.col + direction[0]
                next_row = current_cell.row + direction[1]

                if 0 <= next_col < COLS and 0 <= next_row < ROWS:
                    if self.grid.grid[next_row][next_col].is_barrier():
                        # Carve path between current cell and next cell
                        wall_col = current_cell.col + direction[0] // 2
                        wall_row = current_cell.row + direction[1] // 2
                        self.grid.grid[wall_row][wall_col].reset()
                        self.grid.grid[next_row][next_col].reset()
                        cells.append(self.grid.grid[next_row][next_col])
                        carved_any = True
                        # Draw grid after carving
                        self.draw_grid()
                        break

            if not carved_any:
                cells.remove(current_cell)

class BinaryTree(MazeAlgorithm):
    def start(self):
        self.generate_maze()

    def generate_maze(self):
        for row in range(1, ROWS, 2):
            for col in range(1, COLS, 2):
                self.grid.grid[row][col].reset()

                directions = []
                if col + 2 < COLS:
                    directions.append((2, 0))  # East
                if row + 2 < ROWS:
                    directions.append((0, 2))  # South

                if directions:
                    direction = random.choice(directions)
                    wall_col = col + direction[0] // 2
                    wall_row = row + direction[1] // 2
                    self.grid.grid[wall_row][wall_col].reset()

                # Draw grid after every step
                self.draw_grid()

class Sidewinder(MazeAlgorithm):
    def start(self):
        self.generate_maze()

    def generate_maze(self):
        for row in range(1, ROWS, 2):
            run_set = []

            for col in range(1, COLS, 2):
                self.grid.grid[row][col].reset()  # Reset the current cell (carve the path)
                run_set.append(self.grid.grid[row][col])  # Add current cell to the run set

                # Decide if we should carve east or carve north
                carve_east = (col + 2 < COLS) and (row == 1 or random.choice([True, False]))

                if carve_east:
                    # Carve east
                    next_col = col + 2
                    self.grid.grid[row][next_col].reset()  # Reset the east cell
                    wall_col = col + 1  # Carve the wall between current and east cell
                    self.grid.grid[row][wall_col].reset()
                else:
                    # Carve north
                    if run_set and row > 1:
                        cell_to_carve_north = random.choice(run_set)  # Pick a random cell from the run set
                        self.grid.grid[cell_to_carve_north.row - 2][cell_to_carve_north.col].reset()  # Reset the north cell
                        wall_row = cell_to_carve_north.row - 1  # Carve the wall between current and north cell
                        self.grid.grid[wall_row][cell_to_carve_north.col].reset()
                        run_set = []  # Clear the run set after carving north

                # Draw grid after every step to visualize the progress
                self.draw_grid()
