import pygame
from .constants import *
from .grid import *
from .pathfinding_algorithms import *
from .heuristics import *
from .maze_algorithms import *
from ui import *
from menu_states import *
from algorithms_info import *

class PathfindingVisualizer:
    def __init__(self, window):
        self.window = window
        self.visualizer_grid_area = pygame.Surface((VISUALIZER_GRID_WIDTH, VISUALIZER_GRID_HEIGHT))
        self.visualizer_menu_area = pygame.Surface((VISUALIZER_MENU_WIDTH, VISUALIZER_MENU_HEIGHT))
        self.grid = Grid()
        self.clock = pygame.time.Clock()
        self.start_cell = None
        self.end_cell = None
        self.algorithm = AStarAlgorithm(self.grid.grid, Heuristic.manhattan)  # Default algorithm
        self.heuristic = Heuristic.manhattan  # Default heuristic
        self.maze_algorithm = "custom"  # Default maze algorithm

        # Variables to keep track of the selected buttons
        self.selected_algorithm = "A*"
        self.selected_heuristic = "Manhattan"
        self.selected_maze_algorithm = "Custom"
        self.prompt = "Pick pathfinding algorithm, heuristic, maze algorithm, set start/end points, and run visualization!"
        self.create_menu()

    def create_menu(self):
        """Creates the buttons for the menu using ButtonPrimary."""
        font = pygame.font.SysFont('Verdana', 12)  # Smaller font for buttons
        large_font = pygame.font.SysFont('Verdana', 16)
        
        button_height = 40
        button_x_gap = 10
        button_y_gap = 10
        button_width_3_col = (VISUALIZER_MENU_WIDTH - 30 - 2 * button_x_gap) // 3  # 3 columns
        button_width_2_col = (VISUALIZER_MENU_WIDTH - 30 - button_x_gap) // 2  # 3 columns
        button_width_1_col = (VISUALIZER_MENU_WIDTH - 30)      # 1 columns

        x_absolute_offset = WINDOW_WIDTH - VISUALIZER_MENU_WIDTH
        y_absolute_offset = 150 

        x_menu_center = VISUALIZER_MENU_WIDTH // 2 - VISUALIZER_GRID_MARGIN // 2

        x_relative_offset_button_3_col = x_menu_center - 3 * (button_width_3_col // 2) - button_x_gap
        x_relative_offset_button_2_col = x_menu_center - button_width_2_col - button_x_gap // 2
        x_relative_offset_button_1_col = x_menu_center - button_width_1_col // 2

        self.buttons = {
            "Prompt": ButtonPrimary(
                x_relative_offset_button_1_col, 
                5 + button_height + button_y_gap, 
                button_width_1_col, 
                button_height * 1.4, 
                text=self.prompt, 
                font=font,
                button_color=COLORS['DARK_GREEN'],
                hovered_x=None, hovered_y=None,
                hover_button_color=COLORS['DARK_GREEN'], # Since hover_x and y = None isn't removing the hover ability. 
                text_color=COLORS['LIGHT_CREAM'],
                border_color=COLORS['LIGHT_CREAM']

            ),
            "A*": ButtonPrimary(
                x_relative_offset_button_3_col, 
                y_absolute_offset, 
                button_width_3_col, 
                button_height,
                "A*", font, 
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col, 
                hovered_y=y_absolute_offset
            ),
            "Bi-A*": ButtonPrimary(
                x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                y_absolute_offset, button_width_3_col, 
                button_height, 
                "Bi-A*", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                hovered_y=y_absolute_offset
            ),
            "BFS": ButtonPrimary(
                x_relative_offset_button_3_col + 2 * (button_width_3_col + button_x_gap), 
                y_absolute_offset, button_width_3_col, 
                button_height, 
                "BFS", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + 2 * (button_width_3_col + button_x_gap), 
                hovered_y=y_absolute_offset
            ),
            "DFS": ButtonPrimary(
                x_relative_offset_button_3_col, 
                y_absolute_offset + button_y_gap + button_height, 
                button_width_3_col, 
                button_height, 
                "DFS", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col, 
                hovered_y=y_absolute_offset + button_y_gap + button_height
            ),
            "GBFS": ButtonPrimary(
                x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                y_absolute_offset + button_y_gap + button_height, 
                button_width_3_col, 
                button_height, 
                "GBFS", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                hovered_y=y_absolute_offset + button_y_gap + button_height
            ),
            "JPS": ButtonPrimary(
                x_relative_offset_button_3_col + 2 * (button_width_3_col + button_x_gap), 
                y_absolute_offset + button_y_gap + button_height, button_width_3_col, 
                button_height, 
                "JPS", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + 2 * (button_width_3_col + button_x_gap), 
                hovered_y=y_absolute_offset + button_y_gap + button_height
            ),

            # Heuristics Section
            "Manhattan": ButtonPrimary(
                x_relative_offset_button_2_col, 
                y_absolute_offset + 140, 
                button_width_2_col, 
                button_height, 
                "Manhattan", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_2_col, 
                hovered_y=y_absolute_offset + 140
            ),
            "Euclidean": ButtonPrimary(
                x_relative_offset_button_2_col + button_width_2_col + button_x_gap, 
                y_absolute_offset + 140, 
                button_width_2_col, 
                button_height, 
                "Euclidean", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_2_col + button_width_2_col + button_x_gap, 
                hovered_y=y_absolute_offset + 140
            ),
            "Diagonal": ButtonPrimary(
                x_relative_offset_button_2_col,
                y_absolute_offset + 140 + button_y_gap + button_height, 
                button_width_2_col, 
                button_height,
                "Diagonal", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_2_col , 
                hovered_y=y_absolute_offset + 140 + button_y_gap + button_height
            ),
            "Dijkstra": ButtonPrimary(
                x_relative_offset_button_2_col + button_width_2_col + button_x_gap, 
                y_absolute_offset + 140 + button_y_gap + button_height, 
                button_width_2_col, 
                button_height, 
                "Dijkstra", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_2_col + button_width_2_col + button_x_gap, 
                hovered_y=y_absolute_offset + 140 + button_y_gap + button_height
            ),


            # Maze Generation Algorithms Section
            "Recursive DFS": ButtonPrimary(
                x_relative_offset_button_3_col, 
                y_absolute_offset + 280, 
                button_width_3_col, 
                button_height, 
                "DFS Maze", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col, 
                hovered_y=y_absolute_offset + 280
            ),
            "Growing Tree": ButtonPrimary(
                x_relative_offset_button_3_col + button_width_3_col + 10, 
                y_absolute_offset + 280, button_width_3_col, 
                button_height, 
                "Growing Tree", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + button_width_3_col + 10, 
                hovered_y=y_absolute_offset + 280
            ),
            "Custom": ButtonPrimary(
                x_relative_offset_button_3_col + 2 * (button_width_3_col + 10), 
                y_absolute_offset + 280, 
                button_width_3_col, 
                button_height * 2 + button_y_gap, 
                "Custom", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + 2 * (button_width_3_col + 10), 
                hovered_y=y_absolute_offset + 280
            ),
            "Sidewinder": ButtonPrimary(
                x_relative_offset_button_3_col, y_absolute_offset + 280 + button_height + button_y_gap, 
                button_width_3_col, 
                button_height, 
                "Sidewinder", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col, 
                hovered_y=y_absolute_offset + 280 + button_height + button_y_gap
            ),
            "Binary Tree": ButtonPrimary(
                x_relative_offset_button_3_col + button_width_3_col + 10, 
                y_absolute_offset + 280 + button_height + button_y_gap, 
                button_width_3_col, 
                button_height, 
                "Binary Tree", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + button_width_3_col + 10, 
                hovered_y=y_absolute_offset + 280 + button_height + button_y_gap
            ),

            # Control Buttons
            "Clear Path": ButtonPrimary(
                x_relative_offset_button_2_col, 
                y_absolute_offset + 400, 
                button_width_2_col, 
                button_height, 
                "Clear Path", large_font,
                hovered_x=x_absolute_offset + x_relative_offset_button_1_col,
                hovered_y=y_absolute_offset + 400
            ),
            "Reset Grid": ButtonPrimary(
                x_relative_offset_button_2_col + button_width_2_col + button_x_gap,
                y_absolute_offset + 400, 
                button_width_2_col, 
                button_height, 
                "Reset Grid", large_font,
                hovered_x=x_absolute_offset + x_relative_offset_button_2_col + button_width_2_col + button_x_gap, 
                hovered_y=y_absolute_offset + 400
            ),
            "Start": ButtonPrimary(
                x_relative_offset_button_1_col, 
                y_absolute_offset + 400 + button_height + button_y_gap, 
                button_width_1_col, 
                button_height, 
                "Start", large_font,
                hovered_x=x_absolute_offset + x_relative_offset_button_1_col,
                hovered_y=y_absolute_offset + 400 + button_height + button_y_gap
            ),
            "Back to Menu": ButtonPrimary(
                x_relative_offset_button_3_col,
                y_absolute_offset + 400 + 2* (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                "Back to Menu", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col, 
                hovered_y=y_absolute_offset + 400 + 2* (button_height + button_y_gap)
            ),
            "Algo Details": ButtonPrimary(
                x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                y_absolute_offset + 400 + 2* (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                "Algo Details", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                hovered_y=y_absolute_offset + 400 + 2* (button_height + button_y_gap)
            ),
            "Instructions": ButtonPrimary(
                x_relative_offset_button_3_col + 2 * (button_width_3_col + 10), 
                y_absolute_offset + 400 + 2 * (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                "Instructions", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + 2 * (button_width_3_col + 10), 
                hovered_y=y_absolute_offset + 400 + 2* (button_height + button_y_gap)
            ),
        }

    def run(self):
        # Initial draw with white background
        self.window.fill(COLORS["DARK_GREEN"])
        self.draw_grid()
        self.draw_menu()
        pygame.display.update()
        pygame.time.delay(100) # Prevents clicking by accident when loading

        running = True
        while running:
            self.clock.tick(60)
            input = self.handle_input()
            if input == WELCOME_MENU:
                return WELCOME_MENU
            elif input == PATHFINDER_DETAILS_MENU:
                return PATHFINDER_DETAILS_MENU
            elif input == PATHFINDER_INSTRUCTIONS_MENU:
                return PATHFINDER_INSTRUCTIONS_MENU
            self.draw_grid()
            self.draw_menu()
            pygame.display.update()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Check if any button is clicked
            for name, button in self.buttons.items():
                if button.is_clicked(event):
                    return self.handle_button_click(name)

            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                if self.is_within_grid(mouse_pos):  # Only interact if within grid area
                    cell = self.grid.get_clicked_cell(mouse_pos)
                    if cell:
                        if not self.start_cell and cell != self.end_cell:
                            self.start_cell = cell
                            self.start_cell.make_start()
                        elif not self.end_cell and cell != self.start_cell:
                            self.end_cell = cell
                            self.end_cell.make_end()
                        elif cell != self.start_cell and cell != self.end_cell:
                            cell.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                mouse_pos = pygame.mouse.get_pos()
                if self.is_within_grid(mouse_pos):
                    cell = self.grid.get_clicked_cell(mouse_pos)
                    if cell:
                        cell.reset()

                        if cell == self.start_cell:
                            self.start_cell = None
                        elif cell == self.end_cell:
                            self.end_cell = None

            if event.type == pygame.KEYDOWN:      
                if event.key == pygame.K_SPACE:
                    self.start_pathfinding()
                if event.key == pygame.K_c:
                    self.clear_path()
                if event.key == pygame.K_r:
                    self.reset_grid()

    def handle_button_click(self, name):
        if name in self.buttons:
            if name in ["A*", "Bi-A*", "BFS", "DFS", "GBFS", "JPS"]:
                self.selected_algorithm = name
                self.algorithm = self.get_algorithm_by_name(name)

                # Access the short description from algorithms_info
                short_description = algorithms_info.get(name, {}).get("short_description", "Description not available")
                self.prompt = f"{short_description}"
                self.buttons["Prompt"].update_text(self.prompt)
                self.highlight_selected_buttons()

            elif name in ["Manhattan", "Euclidean", "Diagonal", "Dijkstra"]:
                self.selected_heuristic = name
                self.heuristic = getattr(Heuristic, name.lower())
                self.algorithm = self.get_algorithm_by_name(self.selected_algorithm)

                # Access the short description from algorithms_info
                short_description = algorithms_info.get(name, {}).get("short_description", "Description not available")
                self.prompt = f"{short_description}"
                self.buttons["Prompt"].update_text(self.prompt)
                self.highlight_selected_buttons()

            elif name in ["Recursive DFS", "Growing Tree", "Binary Tree", "Sidewinder", "Custom"]:
                self.selected_maze_algorithm = name
                self.maze_algorithm = name.replace(" ", "")
                print(self.maze_algorithm)
                self.highlight_selected_buttons()

                # Access the short description from algorithms_info
                short_description = algorithms_info.get(name, {}).get("short_description", "Description not available")
                self.prompt = f"{short_description}"
                self.buttons["Prompt"].update_text(self.prompt)

                self.draw_menu()
                self.start_maze_generation(self.maze_algorithm)

            elif name == "Clear Path":
                self.clear_path()
            elif name == "Reset Grid":
                self.reset_grid()
            elif name == "Start":
                self.start_pathfinding()
            elif name == "Back to Menu":
                return self.go_to_main_menu()
            elif name == "Algo Details":
                return self.go_to_algo_details()
            elif name == "Instructions":
                return self.go_to_instructions()

    def highlight_selected_buttons(self):
        """Update the colors of the buttons based on selections."""
        for name in ["A*", "Bi-A*", "BFS", "DFS", "GBFS", "JPS"]:
            button = self.buttons[name]
            button.button_color = COLORS['MEDIUM_GREEN'] if name == self.selected_algorithm else COLORS['LIGHT_GREEN']
            button.text_color = COLORS['LIGHT_TEXT'] if name == self.selected_algorithm else COLORS['DARK_TEXT']

        for name in ["Manhattan", "Euclidean", "Diagonal", "Dijkstra"]:
            button = self.buttons[name]
            button.button_color = COLORS['MEDIUM_GREEN'] if name == self.selected_heuristic else COLORS['LIGHT_GREEN']
            button.text_color = COLORS['LIGHT_TEXT'] if name == self.selected_heuristic else COLORS['DARK_TEXT']

        for name in ["Recursive DFS", "Growing Tree", "Binary Tree", "Sidewinder", "Custom"]:
            button = self.buttons[name]
            button.button_color = COLORS['MEDIUM_GREEN'] if name == self.selected_maze_algorithm else COLORS['LIGHT_GREEN']
            button.text_color = COLORS['LIGHT_TEXT'] if name == self.selected_maze_algorithm else COLORS['DARK_TEXT']

        for name in ["Start", "Back to Menu", "Algo Details"]:
            button = self.buttons[name]
            button.button_color = COLORS['MEDIUM_GREEN'] if name == self.selected_maze_algorithm else COLORS['LIGHT_GREEN']
            button.text_color = COLORS['LIGHT_TEXT'] if name == self.selected_maze_algorithm else COLORS['DARK_TEXT']

    def start_pathfinding(self):
        if not self.algorithm:
            print("No algorithm selected! Press 'a', 'b', or 'd' to choose an algorithm.")        
        elif not self.start_cell or not self.end_cell:
            print("Select starting and ending point!")
        else:
            print("Starting pathfinding...")
            for row in self.grid.grid:
                for cell in row:
                    cell.update_valid_neighbors(self.grid.grid)

            # Find the path and get nodes visited and path length
            nodes_visited, path_length = self.algorithm.find_path(self.start_cell, self.end_cell, self.draw_grid)

            if path_length > 0:
                # Update the prompt text with pathfinding details
                self.prompt = f"Nodes Visited: {nodes_visited} Path Length: {path_length}"
                self.buttons["Prompt"].update_text(self.prompt)  # Update the button with the new prompt text
            else:
                # Update prompt text to indicate path not found
                self.prompt = f"No path found! Nodes Visited: {nodes_visited}"
                self.buttons["Prompt"].update_text(self.prompt)

        print("Pathfinding completed.")
        
    def clear_path(self):
        self.grid.clear_path()
        print("Path cleared. Start, end, and barriers remain.")
        self.prompt = "Nodes Visited:  Path Length: "

    def reset_grid(self):
        self.grid = Grid()
        self.start_cell = None
        self.end_cell = None
        self.algorithm = self.get_algorithm_by_name(self.selected_algorithm)
        self.prompt = "Nodes Visited:  Path Length: "

    def start_maze_generation(self, maze_algorithm):
        self.start_cell = None
        self.end_cell = None  
        self.grid.generate_maze(self.window, maze_algorithm)

    def go_to_main_menu(self):
        print("Going back to the main menu...")
        return WELCOME_MENU

    def go_to_algo_details(self):
        print("Going to the algorithm details page...")
        return PATHFINDER_DETAILS_MENU

    def go_to_instructions(self):
        print("Going to the instructions page...")
        return PATHFINDER_INSTRUCTIONS_MENU
    
    def draw_grid(self):
        self.grid.draw_grid(self.visualizer_grid_area)
        self.window.blit(self.visualizer_grid_area, (0, 0))
        pygame.display.update()

    def draw_menu(self):
        """Creates and draws the buttons and text for the menu."""
        self.visualizer_menu_area.fill(COLORS["DARK_GREEN"])

        text_center_x = (VISUALIZER_MENU_WIDTH - VISUALIZER_GRID_MARGIN) // 2

        # Draw the title and program name
        font_title = pygame.font.SysFont('Verdana', 16, bold=True)
        mini_title_font = pygame.font.SysFont('Verdana', 16)

        draw_text(self.visualizer_menu_area, font_title, "Algo Assist - Pathfinder Visualizer", COLORS['LIGHT_CREAM'], 25, center_x=text_center_x)
        # Draw mini titles for each section
        draw_text(self.visualizer_menu_area, mini_title_font, "Pathfinding Algorithms", COLORS['LIGHT_CREAM'], 120, center_x=text_center_x)
        draw_text(self.visualizer_menu_area, mini_title_font, "Heuristics", COLORS['LIGHT_CREAM'], 260, center_x=text_center_x)
        draw_text(self.visualizer_menu_area, mini_title_font, "Maze Generation Algorithms", COLORS['LIGHT_CREAM'], 400, center_x=text_center_x)

        # Draw all buttons
        for button in self.buttons.values():
            button.draw(self.visualizer_menu_area)

        self.highlight_selected_buttons()

        # Draw the menu area onto the main window
        self.window.blit(self.visualizer_menu_area, (WINDOW_WIDTH - VISUALIZER_MENU_WIDTH, 0))

    def get_algorithm_by_name(self, name):
        algorithms = {
            "A*": AStarAlgorithm(self.grid.grid, self.heuristic),
            "Bi-A*": BiAStarAlgorithm(self.grid.grid, self.heuristic),
            "BFS": BFSAlgorithm(self.grid.grid),
            "DFS": DFSAlgorithm(self.grid.grid),
            "GBFS": GBFSAlgorithm(self.grid.grid, self.heuristic),
            "JPS": JPSAlgorithm(self.grid.grid, self.heuristic)
        }
        return algorithms.get(name)

    def is_within_grid(self, mouse_pos):
        x, y = mouse_pos
        return (VISUALIZER_GRID_MARGIN <= x <= VISUALIZER_GRID_WIDTH + VISUALIZER_GRID_MARGIN and
                VISUALIZER_GRID_MARGIN <= y <= VISUALIZER_GRID_HEIGHT + VISUALIZER_GRID_MARGIN)
