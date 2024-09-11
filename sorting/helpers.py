import pygame
import random
from .sorting_algorithms import *
from .draw_utils import *
from .constants import *
from ui import *
from menu_states import *
from algorithms_info import *

# Utility Functions
def generate_starting_list(n, min_val, max_val):
    """Generates a list of random integers between min_val and max_val and prints the array."""
    lst = [random.randint(min_val, max_val) for _ in range(n)]
    print(f"Generated array: {lst}")
    return lst

def reset_list(visualizer):
    """Resets the list in the visualizer with a new randomly generated list."""
    lst = generate_starting_list(visualizer.state.size, LIST_MIN, LIST_MAX)
    visualizer.set_list(lst)
    visualizer.state.step_mode = False # Reset to regular mode

    # Reinitialize persistent_colors to match the new list size
    visualizer.state.persistent_colors = {i: visualizer.BAR_COLOR for i in range(len(lst))}

def adjust_value(value, adjustment, min_val, max_val):
    """Adjusts a value, ensuring it stays within the allowed range."""
    return max(min_val, min(max_val, value + adjustment))

def initialize_sorting_algorithm(visualizer):
    """Initializes the sorting algorithm generator."""
    # print(f"Initializing sorting algorithm: {visualizer.state.sorting_algo_name}, Ascending: {visualizer.state.ascending}")
    
    # Initialize persistent_colors if it's not already or if the list size changed
    visualizer.state.persistent_colors = {i: visualizer.BAR_COLOR for i in range(len(visualizer.lst))}
    
    generator = visualizer.state.sorting_algorithm(
        visualizer.lst,
        visualizer,
        visualizer.state.persistent_colors,
        visualizer.state.ascending
    )
    
    return generator

# Action Functions
def reset_action(visualizer):
    """Resets the list and reinitializes the sorting algorithm."""
    reset_list(visualizer)
    
    visualizer.state.sorting_algorithm_generator = initialize_sorting_algorithm(visualizer)
    visualizer.state.sorting = False  # Ensure sorting is paused after reset
    
    # Draw the newly reset list with default colors
    draw_list(visualizer, persistent_colors=visualizer.state.persistent_colors)
    
    return visualizer.state.sorting, visualizer.state.sorting_algorithm_generator

def start_or_pause_sorting_action(visualizer):
    """Starts, pauses, or resumes the sorting algorithm based on the current state."""
    if not visualizer.state.sorting:
        if visualizer.state.sorting_algorithm_generator is None:
            visualizer.state.sorting_algorithm_generator = initialize_sorting_algorithm(visualizer)
        
        visualizer.state.sorting = True # Starting sort
    elif visualizer.state.step_mode:
        visualizer.state.step_mode = False # Disable step mode
        visualizer.state.sorting = True # Starting sort
    else:
        visualizer.state.sorting = False # Pausing sort
    
    return visualizer.state.sorting, visualizer.state.sorting_algorithm_generator

def toggle_ascending(visualizer, ascending_value):
    """Toggles between ascending and descending order."""
    visualizer.state.ascending = ascending_value
    visualizer.state.sorting_algorithm_generator = initialize_sorting_algorithm(visualizer)
    return visualizer.state.ascending

def toggle_step_mode(visualizer):
    """Toggle step mode on or off."""
    visualizer.state.step_mode = not visualizer.state.step_mode
    visualizer.state.sorting = True
    
    if visualizer.state.step_mode and visualizer.state.sorting_algorithm_generator is None:
        visualizer.state.sorting_algorithm_generator = initialize_sorting_algorithm(visualizer)

    return visualizer.state.step_mode

def step_forward(visualizer):
    """Advance one step if in step mode."""
    if visualizer.state.step_mode and visualizer.state.sorting:
        # print("Stepping forward one step")
        try:
            next(visualizer.state.sorting_algorithm_generator)
        except StopIteration:
            visualizer.state.sorting = True
    return visualizer

# Event Handling Functions
def handle_keydown(event, visualizer):
    """Handles keydown events and updates the sorting parameters accordingly."""

    print(f"Key pressed: {pygame.key.name(event.key)}")  # Debug: log key pressed

    key_actions = {
        pygame.K_r: lambda: reset_action(visualizer),
        pygame.K_SPACE: lambda: start_or_pause_sorting_action(visualizer),
        pygame.K_a: lambda: toggle_ascending(visualizer, True),
        pygame.K_d: lambda: toggle_ascending(visualizer, False),
        pygame.K_b: lambda: (bubble_sort, "Bubble Sort"),
        pygame.K_i: lambda: (insertion_sort, "Insertion Sort"),
        pygame.K_s: lambda: (selection_sort, "Selection Sort"),
        pygame.K_m: lambda: (merge_sort, "Merge Sort"),
        pygame.K_q: lambda: (quick_sort, "Quick Sort"),
        pygame.K_h: lambda: (heap_sort, "Heap Sort"),
        pygame.K_t: lambda: (tim_sort, "Tim Sort"),
        pygame.K_e: lambda: (tree_sort, "Tree Sort"),
        pygame.K_l: lambda: (shell_sort, "Shell Sort"),
        # pygame.K_g: lambda: (gnome_sort, "Gnome Sort"),
        pygame.K_k: lambda: (cocktail_shaker_sort, "Cocktail Shaker Sort"),
        pygame.K_0: lambda: (comb_sort, "Comb Sort"),
        pygame.K_o: lambda: (bogo_sort, "Bogo Sort"),
        pygame.K_UP: lambda: adjust_value(visualizer.state.speed, LIST_SPEED_INCREMENT, MIN_SPEED, MAX_SPEED),
        pygame.K_DOWN: lambda: adjust_value(visualizer.state.speed, -LIST_SPEED_INCREMENT, MIN_SPEED, MAX_SPEED),
        pygame.K_LEFT: lambda: adjust_value(visualizer.state.size, -LIST_SIZE_INCREMENT, LIST_MIN_SIZE, LIST_MAX_SIZE),
        pygame.K_RIGHT: lambda: adjust_value(visualizer.state.size, LIST_SIZE_INCREMENT, LIST_MIN_SIZE, LIST_MAX_SIZE),
        pygame.K_1: lambda: toggle_step_mode(visualizer),
        pygame.K_2: lambda: step_forward(visualizer),
    }

    if visualizer.state.sorting and event.key not in (pygame.K_SPACE, pygame.K_r, pygame.K_1, pygame.K_2, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT) :
        return visualizer.state

    if event.key in key_actions:
        result = key_actions[event.key]()

        if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            visualizer.state.size = result
            reset_list(visualizer)  # Reset the list and adjust persistent colors
            visualizer.state.sorting_algorithm_generator = initialize_sorting_algorithm(visualizer)
            visualizer.state.sorting = False  # Ensure sorting is paused after resizing
            size_button = visualizer.buttons["Size"]
            size_button.update_text(f"{visualizer.state.size}")

        elif event.key in (pygame.K_r, pygame.K_SPACE):
            visualizer.state.sorting, visualizer.state.sorting_algorithm_generator = result
            # print(f"After key action, generator: {visualizer.state.sorting_algorithm_generator}")
        elif event.key in (pygame.K_a, pygame.K_d):
            visualizer.state.ascending = result
        elif event.key in (
            pygame.K_b, 
            pygame.K_i, 
            pygame.K_s, 
            pygame.K_m, 
            pygame.K_q, 
            pygame.K_h, 
            pygame.K_t, 
            pygame.K_e, 
            pygame.K_l, 
            pygame.K_c, 
            pygame.K_g,
            pygame.K_k,
            pygame.K_0,
            pygame.K_o,
        ):
            visualizer.state.sorting_algorithm, visualizer.state.sorting_algo_name = result
            visualizer.state.sorting_algorithm_generator = initialize_sorting_algorithm(visualizer)
            short_description = algorithms_info.get(visualizer.state.sorting_algo_name, {}).get("short_description", "Description not available")
            visualizer.prompt = f"{visualizer.state.sorting_algo_name} - {short_description}"
            visualizer.buttons["Prompt"].update_text(visualizer.prompt)
        elif event.key in (pygame.K_UP, pygame.K_DOWN):
            visualizer.state.speed = result
            speed_button = visualizer.buttons["Speed"]
            speed_button.update_text(f"{visualizer.state.speed}")
            

        # Only redraw the static UI elements when needed (e.g., when algorithm changes)
        if event.key not in (pygame.K_SPACE, pygame.K_1, pygame.K_2):
            draw(visualizer)

    # print(f"Keydown event handled: {pygame.key.name(event.key)}, Sorting: {visualizer.state.sorting}, Generator type: {type(visualizer.state.sorting_algorithm_generator)}")
    return visualizer.state

def handle_button_click(name, visualizer):
    """Handles button clicks and updates the selected algorithm or control."""
    
    # Define actions for buttons, similar to key_actions
    button_actions = {
        "Bubble Sort": lambda: (bubble_sort, "Bubble Sort"),
        "Insertion Sort": lambda: (insertion_sort, "Insertion Sort"),
        "Selection Sort": lambda: (selection_sort, "Selection Sort"),
        "Cocktail Shaker Sort": lambda: (cocktail_shaker_sort, "Cocktail Shaker Sort"),
        "Comb Sort": lambda: (comb_sort, "Comb Sort"),
        "Shell Sort": lambda: (shell_sort, "Shell Sort"),
        "Merge Sort": lambda: (merge_sort, "Merge Sort"),
        "Quick Sort": lambda: (quick_sort, "Quick Sort"),
        "Tim Sort": lambda: (tim_sort, "Tim Sort"),
        "Heap Sort": lambda: (heap_sort, "Heap Sort"),
        "Tree Sort": lambda: (tree_sort, "Tree Sort"),
        "Bogo Sort": lambda: (bogo_sort, "Bogo Sort"),
        "Ascending": lambda: toggle_ascending(visualizer, True),
        "Descending": lambda: toggle_ascending(visualizer, False),
        "Speed UP": lambda: adjust_value(visualizer.state.speed, LIST_SPEED_INCREMENT, MIN_SPEED, MAX_SPEED),
        "Speed DOWN": lambda: adjust_value(visualizer.state.speed, -LIST_SPEED_INCREMENT, MIN_SPEED, MAX_SPEED),
        "Size UP": lambda: adjust_value(visualizer.state.size, LIST_SIZE_INCREMENT, LIST_MIN_SIZE, LIST_MAX_SIZE),
        "Size DOWN": lambda: adjust_value(visualizer.state.size, -LIST_SIZE_INCREMENT, LIST_MIN_SIZE, LIST_MAX_SIZE),
        "Start / Pause": lambda: start_or_pause_sorting_action(visualizer),
        "Reset List": lambda: reset_action(visualizer),
        "Step Mode": lambda: toggle_step_mode(visualizer),
        "Step Forward": lambda: step_forward(visualizer),
    }

    if name in ["Back to Menu", "Algo Details", "Instructions"]:
                        if name == "Back to Menu":
                            return WELCOME_MENU
                        elif name == "Algo Details":
                            return SORTING_DETAILS_MENU
                        elif name == "Instructions":
                            return SORTING_INSTRUCTIONS_MENU
                        
    if name in button_actions:
        result = button_actions[name]()  # Call the function associated with the button
        
        # Handle algorithm buttons
        if name in ["Bubble Sort", "Insertion Sort", "Selection Sort", "Cocktail Shaker Sort", "Comb Sort", 
                    "Shell Sort", "Merge Sort", "Quick Sort", "Tim Sort", "Heap Sort", "Tree Sort", "Bogo Sort"]:
            visualizer.state.sorting_algorithm, visualizer.state.sorting_algo_name = result
            short_description = algorithms_info.get(name, {}).get("short_description", "Description not available")
            visualizer.prompt = f"{visualizer.state.sorting_algo_name} - {short_description}"
            visualizer.buttons["Prompt"].update_text(visualizer.prompt)
            visualizer.state.sorting_algorithm_generator = initialize_sorting_algorithm(visualizer)

        # Handle other buttons like Ascending/Descending
        elif name in ["Ascending", "Descending"]:
            visualizer.state.ascending = result

        elif name in ["Speed UP", "Speed DOWN"]:
            visualizer.state.speed = button_actions[name]()
            speed_button = visualizer.buttons["Speed"]
            speed_button.update_text(f"{visualizer.state.speed} fps")

        elif name in ["Size UP", "Size DOWN"]:
            visualizer.state.size = button_actions[name]()
            visualizer.state.sorting = False  # Ensure sorting is paused after resizing
            reset_list(visualizer)  # Reset the list and adjust persistent colors
            visualizer.state.sorting_algorithm_generator = initialize_sorting_algorithm(visualizer)
            size_button = visualizer.buttons["Size"]
            size_button.update_text(f"{visualizer.state.size}")

        elif name in ["Start / Pause", "Reset Array"]:
            visualizer.state.sorting, visualizer.state.sorting_algorithm_generator = result
            return True

        else:
            return True

        # Redraw the menu to reflect any changes to button states
        draw(visualizer)

def handle_events(visualizer):
    """Handles all pygame events and updates the sorting state."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            visualizer.state = handle_keydown(event, visualizer)
        for name, button in visualizer.buttons.items():
                if button.is_clicked(event):
                    return handle_button_click(name, visualizer)
    return True

def highlight_selected_buttons(visualizer):
    """Update the colors of the sorting algorithm buttons and control buttons based on selections."""

    # Sorting algorithm buttons
    for name in ["Bubble Sort", "Insertion Sort", "Selection Sort", "Cocktail Shaker Sort", "Comb Sort", 
                "Shell Sort", "Merge Sort", "Quick Sort", "Tim Sort", "Heap Sort", "Tree Sort", "Bogo Sort"]:
        button = visualizer.buttons[name]
        button.button_color = COLORS['MEDIUM_GREEN'] if name == visualizer.state.sorting_algo_name else COLORS['LIGHT_GREEN']
        button.text_color = COLORS['LIGHT_TEXT'] if name == visualizer.state.sorting_algo_name else COLORS['DARK_TEXT']

    # # Control buttons
    for name in ["Ascending", "Descending"]:
        button = visualizer.buttons[name]
        # Check the current sorting order and apply the appropriate color
        if visualizer.state.ascending and name == "Ascending":
            button.button_color = COLORS['MEDIUM_GREEN']
            button.text_color = COLORS['LIGHT_TEXT']
        elif not visualizer.state.ascending and name == "Descending":
            button.button_color = COLORS['MEDIUM_GREEN']
            button.text_color = COLORS['LIGHT_TEXT']
        else:
            button.button_color = COLORS['LIGHT_GREEN']
            button.text_color = COLORS['DARK_TEXT']

    for name in ["Step Mode"]:
        button = visualizer.buttons[name]

        if visualizer.state.step_mode and name == "Step Mode":
            button.button_color = COLORS['MEDIUM_GREEN']
            button.text_color = COLORS['LIGHT_TEXT']
        else:
            button.button_color = COLORS['LIGHT_GREEN']
            button.text_color = COLORS['DARK_TEXT']


            