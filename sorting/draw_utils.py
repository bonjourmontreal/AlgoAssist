import pygame
from ui import *
from .constants import *

def draw(visualizer):
    draw_sorting_section(visualizer)
    visualizer.draw_menu(visualizer)

def draw_sorting_section(visualizer):
    draw_list(visualizer)

def draw_list(visualizer, color_positions=None, persistent_colors=None, comparisons=0, array_accesses=0, swaps=0):
    """
    Draws the list of values as bars in the visualization with a small gap between each bar.
    Also displays the number of comparisons, array accesses, swaps, and the height (value) of each element under the bar
    if the array size is 30 or less.
    """
    if color_positions is None:
        color_positions = {}
    if persistent_colors is None:
        persistent_colors = initialize_persistent_colors(visualizer)

    clear_bars_and_text_area(visualizer)
    persistent_colors = draw_bars(visualizer, color_positions, persistent_colors)
    
    # Only draw the values under the bars if the array size is 30 or less
    if len(visualizer.lst) <= 30:
        draw_value_texts(visualizer)
    
    update_sorting_section_ui(visualizer, comparisons, array_accesses, swaps)

    # Update the display
    pygame.display.update()

    return persistent_colors  # Return updated persistent colors
 
def initialize_persistent_colors(visualizer):
    """Initializes the persistent colors for the bars."""
    return {i: visualizer.GRADIENTS[i % 3] for i in range(len(visualizer.lst))}

def clear_bars_and_text_area(visualizer):
    """Clears the area where the bars and text will be drawn to avoid artifacts."""
    pygame.draw.rect(visualizer.window, visualizer.BACKGROUND_COLOR, (0, 0, SORTING_SECTION_WIDTH, SORTING_SECTION_HEIGHT))

def draw_bars(visualizer, color_positions, persistent_colors):
    """Draws the bars representing the list values."""
    lst = visualizer.lst
    gap_size = visualizer.block_gap_size
    block_width = visualizer.block_width

    min_height = 10  # Minimum height for the smallest bar
    value_range = max(visualizer.max_val - visualizer.min_val, 1)
    
    scale_factor = (SORTING_VISUALISER_HEIGHT - min_height) / value_range

    for i, val in enumerate(lst):
        x = SORTING_VISUAISER_MID_X - visualizer.actual_total_width // 2 + (i * (block_width + gap_size))
        bar_height = (val - visualizer.min_val) * scale_factor + min_height
        val_text_height = 20
        y = SORTING_VISUALISER_END_Y - bar_height - val_text_height

        color = persistent_colors[i] = color_positions.get(i, persistent_colors[i])
        pygame.draw.rect(visualizer.window, color, (x, y, block_width, bar_height))

    return persistent_colors

def draw_value_texts(visualizer):
    """Draws the height (value) of each element under the bar."""
    lst = visualizer.lst
    gap_size = visualizer.block_gap_size
    block_width = visualizer.block_width

    for i, val in enumerate(lst):
        x = SORTING_VISUAISER_MID_X - visualizer.actual_total_width // 2 + (i * (block_width + gap_size))
        y_offset = 20
        y = SORTING_VISUALISER_END_Y - y_offset

        value_text = visualizer.SMALL_FONT.render(str(val), True, visualizer.TEXT_COLOR)
        text_x = x + (block_width - value_text.get_width()) // 2
        text_y = y

        pygame.draw.rect(visualizer.window, visualizer.BACKGROUND_COLOR, 
                         (x, text_y - 5, block_width, value_text.get_height() + 5))
        visualizer.window.blit(value_text, (text_x, text_y))

def update_sorting_section_ui(visualizer, comparisons, array_accesses, swaps):
    draw_title(visualizer)
    draw_size_speed(visualizer)
    draw_comparisons_accesses(visualizer, comparisons, array_accesses, swaps)
    draw_visualizer_border(visualizer)

def draw_title(visualizer):
    """Draws the title of the sorting algorithm below the main title."""
    title = visualizer.LARGE_FONT.render(
        f"{visualizer.state.sorting_algo_name}", 
        True, 
        visualizer.TEXT_COLOR
    )
    visualizer.window.blit(title, (SORTING_VISUALISER_START_X + 15, SORTING_SECTION_MARGIN * 2))  # Adjusted y position

def draw_size_speed(visualizer):
    """Draws the number of comparisons, array accesses, and swaps with a fixed left alignment above the bars."""
    text_y_position = SORTING_SECTION_MARGIN * 2 - 5 # Adjust this value to move the text just above the bars
    fixed_x_position = SORTING_VISUALISER_END_X - 320  # Adjust this value to set the fixed left alignment

    # Render the text
    comparisons_text = visualizer.FONT.render(f"Size: {visualizer.state.size}", True, visualizer.TEXT_COLOR)
    array_accesses_text = visualizer.FONT.render(f"Speed: {visualizer.state.speed} fps", True, visualizer.TEXT_COLOR)

    # Calculate the width of the clearing area based on the width of the text
    clearing_width = max(comparisons_text.get_width(), array_accesses_text.get_width()) + 20  # Adding some padding

    # Clear only the area where the text will be drawn
    text_height = comparisons_text.get_height() + array_accesses_text.get_height()
    pygame.draw.rect(visualizer.window, visualizer.BACKGROUND_COLOR, 
                     (fixed_x_position, text_y_position, clearing_width, text_height))

    # Draw the text on the screen with a fixed starting position
    visualizer.window.blit(comparisons_text, (fixed_x_position, text_y_position))
    visualizer.window.blit(array_accesses_text, (fixed_x_position, text_y_position + 20))

def draw_comparisons_accesses(visualizer, comparisons, array_accesses, swaps):
    """Draws the number of comparisons, array accesses, and swaps with a fixed left alignment above the bars."""
    fixed_x_position = SORTING_VISUALISER_END_X - 180  # Adjust this value to set the fixed left alignment
    text_y_position = SORTING_SECTION_MARGIN * 2 - 5 # Adjust this value to move the text just above the bars

    # Render the text
    comparisons_text = visualizer.FONT.render(f"Comparisons: {comparisons}", True, visualizer.TEXT_COLOR)
    array_accesses_text = visualizer.FONT.render(f"Array Accesses: {array_accesses}", True, visualizer.TEXT_COLOR)
    swaps_text = visualizer.FONT.render(f"Swaps: {swaps}", True, visualizer.TEXT_COLOR)

    # Calculate the width of the clearing area based on the width of the text
    clearing_width = max(comparisons_text.get_width(), array_accesses_text.get_width(), swaps_text.get_width()) + 20  # Adding some padding

    # Clear only the area where the text will be drawn
    text_height = comparisons_text.get_height() + array_accesses_text.get_height() + swaps_text.get_height()
    pygame.draw.rect(visualizer.window, visualizer.BACKGROUND_COLOR, 
                     (fixed_x_position, text_y_position, clearing_width, text_height))

    # Draw the text on the screen with a fixed starting position
    visualizer.window.blit(comparisons_text, (fixed_x_position, text_y_position))
    visualizer.window.blit(array_accesses_text, (fixed_x_position, text_y_position + 20))
    # visualizer.window.blit(swaps_text, (fixed_x_position, text_y_position))

def draw_visualizer_border(visualizer):
    # Draw a thicker black border around the grid
    border_thickness = 4  # Thickness of the border
    pygame.draw.rect(
        visualizer.window, 
        COLORS["LIGHT_GREEN"], 
        (SORTING_SECTION_MARGIN - border_thickness // 2, 
        SORTING_SECTION_MARGIN - border_thickness // 2, 
        SORTING_VISUALISER_WIDTH + 2 * SORTING_SECTION_MARGIN - border_thickness // 2, 
        SORTING_SECTION_HEIGHT - border_thickness // 2), 
        border_thickness
    )






