import pygame
import math
from dataclasses import dataclass
from .sorting_algorithms import *
from .helpers import *
from .draw_utils import *
from ui import *
from .constants import *
from menu_states import *
from algorithms_info import *

pygame.init()

class SortingVisualizer:
    """Handles the visualization settings and configurations."""
    
    # General Colors
    BACKGROUND_COLOR = COLORS["DARK_GREEN"]
    TEXT_COLOR = COLORS["LIGHT_CREAM"]

    # Sorting Colors
    SORTED_COLOR = (0, 230, 0)  # Softer Green
    COMPARISON_COLOR = (230, 0, 0)  # Softer Red
    PRIMARY_ACTIVE_COLOR = (255, 255, 102)  # Softer Yellow
    SECONDARY_ACTIVE_COLOR = (51, 102, 255)  # Softer Blue
    BAR_COLOR = COLORS["LIGHT_GREEN"]

    # Gradient Colors (Bars in the sorting visualization)
    GRADIENT_DARK = COLORS["LIGHT_GREEN"]
    GRADIENT_MEDIUM = COLORS["LIGHT_GREEN"]
    GRADIENT_LIGHT = COLORS["LIGHT_GREEN"]
    GRADIENTS = [GRADIENT_MEDIUM, GRADIENT_MEDIUM, GRADIENT_MEDIUM]

    SMALL_FONT = pygame.font.SysFont('Verdana', 12)
    FONT = pygame.font.SysFont('Verdana', 16)
    LARGE_FONT = pygame.font.SysFont('Verdana', 20)
    XLARGE_FONT = pygame.font.SysFont('Verdana', 48)

    def __init__(self, width, height, lst, state):
        """Initializes the drawing information with the screen size and list."""
        self.width = width
        self.height = height
        self.state = state
        self.set_list(lst)

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")

        self.visualizer_menu_area = pygame.Surface((MENU_SECTION_WIDTH, MENU_SECTION_HEIGHT))
        short_description = algorithms_info.get(self.state.sorting_algo_name, {}).get("short_description", "Description not available")
        self.prompt = f"{self.state.sorting_algo_name} - {short_description}"
        self.create_menu()

    def set_list(self, lst):
        """Sets the list and calculates block sizes."""
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_height = math.floor((SORTING_VISUALISER_HEIGHT) / (self.max_val - self.min_val))
        self.block_gap_size = 2
        self.total_gaps_width = (len(lst) - 1) * self.block_gap_size
        self.block_width = round((SORTING_VISUALISER_WIDTH - self.total_gaps_width) / len(lst))
        self.actual_total_width = self.block_width * len(lst) + self.block_gap_size * (len(lst) - 1) # Used for ensuring centered output in frame

    # TODO get_color_for_depth, create_menu and draw_menu should be moved to draw_utils.py (but currently causing many bugs if done)
    def get_color_for_depth(self, depth):
        """Returns a color based on the depth of the binary tree for heap sort."""
        depth_colors = [
            (255, 255, 204),  # Light yellow for depth 0
            (255, 179, 71),   # Bright orange
            (255, 102, 102),  # Bright red
            (255, 102, 255),  # Bright pink
            (178, 102, 255),  # Bright violet
            (102, 102, 255),  # Bright blue
            (102, 178, 255),  # Bright sky blue
            (102, 255, 102),  # Bright green
            (153, 255, 51),   # Bright lime green
            (51, 204, 51)     # Bright emerald green
        ]
        return depth_colors[depth % len(depth_colors)]
    
    def create_menu(self):
        """Creates the buttons for the menu using ButtonPrimary."""
        font = pygame.font.SysFont('Verdana', 12)  # Smaller font for buttons
        large_font = pygame.font.SysFont('Verdana', 16)
        
        button_height = 40
        button_x_gap = 10
        button_y_gap = 10
        button_width_3_col = (MENU_SECTION_WIDTH - 30 - 2 * button_x_gap) // 3  # 3 columns
        button_width_2_col = (MENU_SECTION_WIDTH - 30 - button_x_gap) // 2  # 3 columns
        button_width_1_col = (MENU_SECTION_WIDTH - 30)      # 1 columns

        x_absolute_offset = WINDOW_WIDTH - MENU_SECTION_WIDTH
        y_absolute_offset_algorithms = 160 
        y_absolute_offset_controls = 395

        x_menu_center = MENU_SECTION_WIDTH // 2

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
            "Bubble Sort": ButtonPrimary(
                x_relative_offset_button_3_col, 
                y_absolute_offset_algorithms, 
                button_width_3_col, 
                button_height,
                "Bubble Sort", font, 
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col, 
                hovered_y=y_absolute_offset_algorithms
            ),
            "Insertion Sort": ButtonPrimary(
                x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                y_absolute_offset_algorithms, button_width_3_col, 
                button_height, 
                "Insertion Sort", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                hovered_y=y_absolute_offset_algorithms
            ),
            "Selection Sort": ButtonPrimary(
                x_relative_offset_button_3_col + 2 * (button_width_3_col + button_x_gap), 
                y_absolute_offset_algorithms, button_width_3_col, 
                button_height, 
                "Selection Sort", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + 2 * (button_width_3_col + button_x_gap), 
                hovered_y=y_absolute_offset_algorithms
            ),
            "Cocktail Shaker Sort": ButtonPrimary(
                x_relative_offset_button_3_col, 
                y_absolute_offset_algorithms + button_y_gap + button_height, 
                button_width_3_col, 
                button_height, 
                "Cocktail Shaker Sort", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col, 
                hovered_y=y_absolute_offset_algorithms + button_y_gap + button_height
            ),
            "Comb Sort": ButtonPrimary(
                x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                y_absolute_offset_algorithms + button_y_gap + button_height, 
                button_width_3_col, 
                button_height, 
                "Comb Sort", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                hovered_y=y_absolute_offset_algorithms + button_y_gap + button_height
            ),
            "Shell Sort": ButtonPrimary(
                x_relative_offset_button_3_col + 2 * (button_width_3_col + button_x_gap), 
                y_absolute_offset_algorithms + button_y_gap + button_height, button_width_3_col, 
                button_height, 
                "Shell Sort", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + 2 * (button_width_3_col + button_x_gap), 
                hovered_y=y_absolute_offset_algorithms + button_y_gap + button_height
            ),
            "Merge Sort": ButtonPrimary(
                x_relative_offset_button_3_col, 
                y_absolute_offset_algorithms + 2 * (button_y_gap + button_height), 
                button_width_3_col, 
                button_height, 
                "Merge Sort", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col, 
                hovered_y=y_absolute_offset_algorithms + 2 * (button_y_gap + button_height)
            ),
            "Quick Sort": ButtonPrimary(
                x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                y_absolute_offset_algorithms + 2 * (button_y_gap + button_height), 
                button_width_3_col, 
                button_height, 
                "Quick Sort", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                hovered_y=y_absolute_offset_algorithms + 2 * (button_y_gap + button_height)
            ),
            "Tim Sort": ButtonPrimary(
                x_relative_offset_button_3_col + 2 * (button_width_3_col + button_x_gap), 
                y_absolute_offset_algorithms + 2 * (button_y_gap + button_height), button_width_3_col, 
                button_height, 
                "Tim Sort", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + 2 * (button_width_3_col + button_x_gap), 
                hovered_y=y_absolute_offset_algorithms + 2 * (button_y_gap + button_height)
            ),
            "Heap Sort": ButtonPrimary(
                x_relative_offset_button_3_col, 
                y_absolute_offset_algorithms + 3 * (button_y_gap + button_height), 
                button_width_3_col, 
                button_height, 
                "Heap Sort", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col, 
                hovered_y=y_absolute_offset_algorithms + 3 * (button_y_gap + button_height)
            ),
            "Tree Sort": ButtonPrimary(
                x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                y_absolute_offset_algorithms + 3 * (button_y_gap + button_height), 
                button_width_3_col, 
                button_height, 
                "Tree Sort", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                hovered_y=y_absolute_offset_algorithms + 3 * (button_y_gap + button_height)
            ),
            "Bogo Sort": ButtonPrimary(
                x_relative_offset_button_3_col + 2 * (button_width_3_col + button_x_gap), 
                y_absolute_offset_algorithms + 3 * (button_y_gap + button_height), button_width_3_col, 
                button_height, 
                "Bogo Sort", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + 2 * (button_width_3_col + button_x_gap), 
                hovered_y=y_absolute_offset_algorithms + 3 * (button_y_gap + button_height)
            ),

            # Control Buttons
            "Ascending": ButtonPrimary(
                x_relative_offset_button_2_col, 
                y_absolute_offset_controls, 
                button_width_2_col, 
                button_height, 
                "Ascending", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_1_col,
                hovered_y=y_absolute_offset_controls
            ),
            "Descending": ButtonPrimary(
                x_relative_offset_button_2_col + button_width_2_col + button_x_gap,
                y_absolute_offset_controls, 
                button_width_2_col, 
                button_height, 
                "Descending", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_2_col + button_width_2_col + button_x_gap, 
                hovered_y=y_absolute_offset_controls
            ),
            "Speed DOWN": ButtonPrimary(
                x_relative_offset_button_3_col, 
                y_absolute_offset_controls + (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                "Speed DOWN", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col, 
                hovered_y=y_absolute_offset_controls + (button_height + button_y_gap)
            ),
            "Speed": ButtonPrimary(
                x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                y_absolute_offset_controls + (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                text=f"{self.state.speed} fps", 
                font=font,
                button_color=COLORS['DARK_GREEN'],
                hovered_x=None, hovered_y=None,
                hover_button_color=COLORS['DARK_GREEN'], # Since hover_x and y = None isn't removing the hover ability. 
                text_color=COLORS['LIGHT_CREAM'],
                border_color=COLORS['LIGHT_CREAM']
            ),
            "Speed UP": ButtonPrimary(
                x_relative_offset_button_3_col + 2 * (button_width_3_col + 10),
                y_absolute_offset_controls + (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                "Speed UP", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + 2 * (button_width_3_col + 10), 
                hovered_y=y_absolute_offset_controls + (button_height + button_y_gap)
            ),
            "Size DOWN": ButtonPrimary(
                x_relative_offset_button_3_col, 
                y_absolute_offset_controls + 2 * (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                "Size DOWN", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col, 
                hovered_y=y_absolute_offset_controls + 2 * (button_height + button_y_gap)
            ),
            "Size": ButtonPrimary(
                x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                y_absolute_offset_controls + 2 * (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                text=f"{self.state.size}", 
                font=font,
                button_color=COLORS['DARK_GREEN'],
                hovered_x=None, hovered_y=None,
                hover_button_color=COLORS['DARK_GREEN'], # Since hover_x and y = None isn't removing the hover ability. 
                text_color=COLORS['LIGHT_CREAM'],
                border_color=COLORS['LIGHT_CREAM']
            ),
            "Size UP": ButtonPrimary(
                x_relative_offset_button_3_col + 2 * (button_width_3_col + 10),
                y_absolute_offset_controls + 2 * (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                "Size UP", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + 2 * (button_width_3_col + 10), 
                hovered_y=y_absolute_offset_controls + 2 * (button_height + button_y_gap)
            ),
            "Reset List": ButtonPrimary(
                x_relative_offset_button_3_col,
                y_absolute_offset_controls + 3 * (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                "Reset List", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col, 
                hovered_y=y_absolute_offset_controls + 3 * (button_height + button_y_gap)
            ),
            "Step Mode": ButtonPrimary(
                x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                y_absolute_offset_controls + 3 * (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                "Step Mode", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                hovered_y=y_absolute_offset_controls + 3 * (button_height + button_y_gap)
            ),
            "Step Forward": ButtonPrimary(
                x_relative_offset_button_3_col + 2 * (button_width_3_col + 10), 
                y_absolute_offset_controls + 3 * (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                "Step Forward", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + 2 * (button_width_3_col + 10), 
                hovered_y=y_absolute_offset_controls + 3 * (button_height + button_y_gap)
            ),
            "Start / Pause": ButtonPrimary(
                x_relative_offset_button_1_col, 
                y_absolute_offset_controls + 4 * (button_height + button_y_gap), 
                button_width_1_col, 
                button_height, 
                "Start / Pause", large_font,
                hovered_x=x_absolute_offset + x_relative_offset_button_1_col,
                hovered_y=y_absolute_offset_controls + 4 * (button_height + button_y_gap)
            ),
            "Back to Menu": ButtonPrimary(
                x_relative_offset_button_3_col,
                y_absolute_offset_controls + 5 * (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                "Back to Menu", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col, 
                hovered_y=y_absolute_offset_controls + 5 * (button_height + button_y_gap)
            ),
            "Algo Details": ButtonPrimary(
                x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                y_absolute_offset_controls + 5 * (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                "Algo Details", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + button_width_3_col + button_x_gap, 
                hovered_y=y_absolute_offset_controls + 5 * (button_height + button_y_gap)
            ),
            "Instructions": ButtonPrimary(
                x_relative_offset_button_3_col + 2 * (button_width_3_col + 10), 
                y_absolute_offset_controls + 5 * (button_height + button_y_gap), 
                button_width_3_col, 
                button_height, 
                "Instructions", font,
                hovered_x=x_absolute_offset + x_relative_offset_button_3_col + 2 * (button_width_3_col + 10), 
                hovered_y=y_absolute_offset_controls + 5 * (button_height + button_y_gap)
            ),
        }

    def draw_menu(self, visualizer):
        """Creates and draws the buttons and text for the menu."""
        self.visualizer_menu_area.fill(COLORS["DARK_GREEN"])

        text_center_x = (MENU_SECTION_WIDTH) // 2
        font_title = pygame.font.SysFont('Verdana', 16, bold=True)
        mini_title_font = pygame.font.SysFont('Verdana', 16)

        draw_text(self.visualizer_menu_area, font_title, "Algo Assist - Sorting Visualizer", COLORS['LIGHT_CREAM'], 25, center_x=text_center_x)
        draw_text(self.visualizer_menu_area, mini_title_font, "Sorting Algorithms", COLORS['LIGHT_CREAM'], 130, center_x=text_center_x)
        draw_text(self.visualizer_menu_area, mini_title_font, "Controls", COLORS['LIGHT_CREAM'], 365, center_x=text_center_x)

        for button in self.buttons.values():
            button.draw(self.visualizer_menu_area)

        highlight_selected_buttons(visualizer)

        # Draw the menu area onto the main window
        self.window.blit(self.visualizer_menu_area, (WINDOW_WIDTH - MENU_SECTION_WIDTH, 0))

    def run(self, visualizer):
        pygame.init()
        clock = pygame.time.Clock()

        visualizer.window.fill(COLORS["DARK_GREEN"])
        draw(visualizer)

        running = True
        while running:
            clock.tick(visualizer.state.speed)
            input = handle_events(visualizer)

            if input == WELCOME_MENU:
                return WELCOME_MENU
            elif input == SORTING_DETAILS_MENU:
                return SORTING_DETAILS_MENU
            elif input == SORTING_INSTRUCTIONS_MENU:
                return SORTING_INSTRUCTIONS_MENU
            elif input == False:
                running = False
                continue # Skip further execution in this iteration

            if visualizer.state.sorting and visualizer.state.sorting_algorithm_generator:
                if not visualizer.state.step_mode:
                    try:
                        next(visualizer.state.sorting_algorithm_generator)
                    except StopIteration:
                        visualizer.state.sorting = False

            self.draw_menu(visualizer) # Redraw everyframe to allow button hover action (could be made more efficient with redrawing just the button on hover)
            pygame.display.update()

        pygame.quit()
        quit()

@dataclass
class SortingState:
    sorting: bool
    sorting_algorithm_generator: any
    sorting_algo_name: str
    sorting_algorithm: any
    ascending: bool
    speed: int
    size: int
    step_mode: bool = False
    persistent_colors: dict = None 

def initialize_sorting_visualizer(size, speed, sorting_algorithm, sorting_algo_name):
    "Initializes and returns the sorting visualizer and its state."
    lst = generate_starting_list(size, LIST_MIN, LIST_MAX)
    state = SortingState(
        sorting=False,
        sorting_algorithm_generator=None,
        sorting_algo_name=sorting_algo_name, # The name: "Bubble Sort"
        sorting_algorithm=sorting_algorithm, # The function "bubble_sort"
        ascending=True,
        speed=speed,
        size=size,
        step_mode=False,
        persistent_colors=None,
    )
    visualizer = SortingVisualizer(WINDOW_WIDTH, WINDOW_HEIGHT, lst, state)
    
    return visualizer
