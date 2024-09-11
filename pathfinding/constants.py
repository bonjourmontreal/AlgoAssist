# Default values for the window and grid dimensions for pathfinding app
WINDOW_WIDTH = 1060
WINDOW_HEIGHT = 720
GRID_WIDTH = 660
GRID_HEIGHT = 660

# Calculate the margin to center the visualizer vertically and add to the left margin
VISUALIZER_GRID_MARGIN = (WINDOW_HEIGHT - GRID_HEIGHT) // 2 # 30px margin

# Define the visualizer area
VISUALIZER_GRID_WIDTH = GRID_WIDTH + 2 * VISUALIZER_GRID_MARGIN
VISUALIZER_GRID_HEIGHT = WINDOW_HEIGHT

# Define the side menu area
VISUALIZER_MENU_WIDTH = WINDOW_WIDTH - VISUALIZER_GRID_WIDTH
VISUALIZER_MENU_HEIGHT = WINDOW_HEIGHT

# Constants for grid and window dimensions
COLS, ROWS = 33, 33

# Define the dimensions of each cell in the grid based on the visualizer area
CELL_WIDTH, CELL_HEIGHT = GRID_WIDTH // COLS, GRID_HEIGHT // ROWS

