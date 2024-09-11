import random
from .constants import *
from .maze_algorithms import RecursiveDFS, GrowingTree, BinaryTree, Sidewinder
from ui import *

class Cell:
    def __init__(self, col, row) -> None:
        self.col = col
        self.row = row
        self.width = CELL_WIDTH
        self.height = CELL_HEIGHT
        self.x = col * CELL_WIDTH + VISUALIZER_GRID_MARGIN  # Adjusted x position during initialization
        self.y = row * CELL_HEIGHT + VISUALIZER_GRID_MARGIN  # Adjusted y position during initialization
        self.color = COLORS["LIGHT_CREAM"]
        self.valid_neighbors = []

    def get_pos(self):
        return self.col, self.row

    def draw_cell(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    # Checks if the cell is closed (processed)
    def is_closed(self):
        return self.color == COLORS["RED"]
    
    # Checks if the cell is open (in the queue)
    def is_open(self):
        return self.color == COLORS["GREEN"]
    
    def is_barrier(self):
        return self.color == COLORS["BLACK"]
    
    def is_start(self):
        return self.color == COLORS["ORANGE"]
    
    def is_end(self):
        return self.color == COLORS["TURQUOISE"]
    
    # Resets the cell to its initial state
    def reset(self):
        self.color = COLORS["LIGHT_CREAM"]

    # Changes the cell color to represent different states
    def make_closed(self):
        self.color = COLORS["RED"]
    
    def make_open(self):
        self.color = COLORS["GREEN"]
    
    def make_barrier(self):
        self.color = COLORS["BLACK"]
    
    def make_start(self):
        self.color = COLORS["ORANGE"]
    
    def make_end(self):
        self.color = COLORS["TURQUOISE"]

    def make_path(self):
        self.color = COLORS["PURPLE"]
        
    def update_valid_neighbors(self, grid):
        self.valid_neighbors = []  # Clear previous neighbors

        # Check each direction for valid neighbors (not barriers)
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.valid_neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.valid_neighbors.append(grid[self.row - 1][self.col])

        if self.col < COLS - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.valid_neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.valid_neighbors.append(grid[self.row][self.col - 1])

# Manages the grid of cells
class Grid:
    def __init__(self):
        self.grid = self.initialize_grid()
        self.drawn_grid = False

    def initialize_grid(self):
        grid = [[Cell(col, row) for col in range(COLS)] for row in range(ROWS)]
        return grid

    def generate_maze(self, window, algorithm):
        # Clear the grid by making all cells barriers before generating the maze
        for row in self.grid:
            for cell in row:
                cell.make_barrier()

        # Dispatch the appropriate algorithm
        maze_generator = self.get_maze_algorithm(algorithm, window)

        # Start maze generation if the algorithm exists
        if maze_generator:
            maze_generator.start()

    def get_maze_algorithm(self, algorithm, window):
        if algorithm == 'RecursiveDFS':
            return RecursiveDFS(self, window)
        elif algorithm == 'GrowingTree':
            return GrowingTree(self, window)
        elif algorithm == 'BinaryTree':
            return BinaryTree(self, window)
        elif algorithm == 'Sidewinder':
            return Sidewinder(self, window)
        elif algorithm == 'Custom':
            self.clear_grid()  # Custom case, just reset the grid without barriers
            return None

    def clear_grid(self):
        # Resets all cells to be empty
        for row in self.grid:
            for cell in row:
                cell.reset()

    # Draws the grid cells and grid lines on the window
    def draw_grid(self, window):
        if self.drawn_grid == False:
            window.fill(COLORS["DARK_GREEN"])
            self.drawn_grid = True

        # Draw all grid cells
        for row in self.grid:
            for cell in row:
                cell.draw_cell(window)

        # Draw grid lines with the same dynamic margins
        for col in range(COLS + 1):  # Ensure the last column line is drawn
            pygame.draw.line(window, COLORS["GREY"], 
                            (col * CELL_WIDTH + VISUALIZER_GRID_MARGIN, VISUALIZER_GRID_MARGIN), 
                            (col * CELL_WIDTH + VISUALIZER_GRID_MARGIN, GRID_HEIGHT + VISUALIZER_GRID_MARGIN))
        for row in range(ROWS + 1):  # Ensure the last row line is drawn
            pygame.draw.line(window, COLORS["GREY"], 
                            (VISUALIZER_GRID_MARGIN, row * CELL_HEIGHT + VISUALIZER_GRID_MARGIN), 
                            (GRID_WIDTH + VISUALIZER_GRID_MARGIN, row * CELL_HEIGHT + VISUALIZER_GRID_MARGIN))

        # Draw a thicker black border around the grid
        border_thickness = 4  # Thickness of the border
        pygame.draw.rect(
            window, 
            COLORS["LIGHT_GREEN"], 
            (VISUALIZER_GRID_MARGIN - border_thickness, 
            VISUALIZER_GRID_MARGIN - border_thickness, 
            GRID_WIDTH + border_thickness * 2, 
            GRID_HEIGHT + border_thickness * 2), 
            border_thickness
        )

        pygame.display.update()  # Update the display here

    def get_clicked_cell(self, mouse_pos):
        x, y = mouse_pos
        col = int((x - VISUALIZER_GRID_MARGIN) / CELL_WIDTH)
        row = int((y - VISUALIZER_GRID_MARGIN) / CELL_HEIGHT)

        # Ensure the calculated col and row are within the grid bounds
        if col < 0 or col >= COLS or row < 0 or row >= ROWS:
            return None  # Return None if the click is out of bounds

        return self.grid[row][col]

    def clear_path(self):
        for row in self.grid:
            for cell in row:
                if not (cell.is_start() or cell.is_end() or cell.is_barrier()):
                    cell.reset()
