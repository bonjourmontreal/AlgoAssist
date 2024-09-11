import pygame
from ui import *
from sorting import main as sorting_main
from pathfinding import main as pathfinding_main
from menu_states import *
from algorithms_info import *

# Menu and Details Configuration
menu_config = {
    "welcome_menu": {
        "state": WELCOME_MENU,
    },
    "pathfinder_menu": {
        "state": PATHFINDER_MENU,
        "details_menu": {
            "title": "Pathfinding Algorithms",
            "description": "Details about various pathfinding algorithms...",
            "back_menu": PATHFINDER_MENU
        },
        "instructions_menu": PATHFINDER_INSTRUCTIONS_MENU
    },
    "sorting_menu": {
        "state": SORTING_MENU,
        "details_menu": {
            "title": "Sorting Algorithms",
            "description": "Details about various sorting algorithms...",
            "back_menu": SORTING_MENU
        },
        "instructions_menu": SORTING_INSTRUCTIONS_MENU
    },
}

def main_menu(window):
    screen_width, screen_height = window.get_size()

    # Fonts
    title_font = pygame.font.SysFont('Verdana', 60, bold=True)
    desc_font = pygame.font.SysFont('Verdana', 20)

    # Text content
    title_text = "Welcome to AlgoAssist"
    description_text = (
        "AlgoAssist is an intuitive tool designed for visualizing and understanding "
        "various pathfinding and sorting algorithms. Explore the fascinating world of algorithms "
        "with interactive visualizations and gain deeper insights into how they work."
    )

    # Title position
    title_y = 60
    title_x = (screen_width - title_font.size(title_text)[0]) // 2

    # Description configuration
    gap_between_title_and_description = 30
    description_y = title_y + title_font.get_height() + gap_between_title_and_description
    description_max_width = screen_width - 200

    # Calculate the height of the wrapped description text
    wrapped_lines = wrap_text(description_text, desc_font, description_max_width)
    total_text_height = len(wrapped_lines) * desc_font.get_height()

    # Button configuration
    button_width = 500
    button_height = 80
    gap_after_description = 50 
    button_gap = 30

    # Calculate button positions
    first_button_y = description_y + total_text_height + gap_after_description
    button_x = (screen_width - button_width) // 2  # Center button horizontally

    # Button texts and their corresponding menus
    button_texts = ["Sorting Algorithms", "Pathfinding Algorithms", "Quit"]
    button_menu_map = {
        "Sorting Algorithms": SORTING_MENU,
        "Pathfinding Algorithms": PATHFINDER_MENU,
        "Quit": None  # Quit the application
    }

    # Create buttons and position them
    buttons = []
    for i, text in enumerate(button_texts):
        button_y = first_button_y + i * (button_height + button_gap)
        buttons.append(ButtonPrimary(button_x, button_y, button_width, button_height, text))

    # Draw the initial screen
    window.fill(COLORS['DARK_GREEN'])
    draw_text(window, title_font, title_text, COLORS['LIGHT_TEXT'], title_y, center_x=screen_width // 2)
    draw_text(window, desc_font, description_text, COLORS['LIGHT_TEXT'], description_y, max_width=description_max_width, center_x=screen_width // 2)
    pygame.display.update()

    # Main loop to handle button interactions
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Check if any button is clicked
            for button in buttons:
                if button.is_clicked(event):
                    if button.text == "Quit":
                        pygame.quit()
                        quit()
                    return button_menu_map.get(button.text, WELCOME_MENU)  # Returns mapped menu or WELCOME_MENU if not found

        # Draw buttons
        for button in buttons:
            button.draw(window)

        pygame.display.update()

def generic_menu(window, title, buttons_config):
    screen_width, screen_height = window.get_size()

    # Title
    title_font = pygame.font.SysFont('Verdana', 60, bold=True)
    title_text = title_font.render(title, True, COLORS['LIGHT_TEXT'])
    title_x, title_y = center_element(screen_width, title_text.get_width(), 60)
    
    # Calculate button positions
    button_width = 500
    button_height = 80
    first_button_y = screen_height // 2 - 150
    button_gap = 100

    buttons = []
    for i, (text, action) in enumerate(buttons_config):
        button_y = first_button_y + i * button_gap
        button_x = center_element(screen_width, button_width, button_y)[0]
        buttons.append(ButtonPrimary(button_x, button_y, button_width, button_height, text))

    window.fill(COLORS['DARK_GREEN'])
    window.blit(title_text, (title_x, title_y))

    while True:
        for button in buttons:
            button.draw(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            for button, (text, action) in zip(buttons, buttons_config):
                if button.is_clicked(event):
                    return action()

        pygame.display.update()

def pathfinder_menu(window):
    return generic_menu(
        window,
        "Pathfinder Menu",
        [
            ("Launch Visualizer", lambda: pathfinding_main.launch_visualizer(window) or PATHFINDER_MENU),
            ("Instructions", lambda: PATHFINDER_INSTRUCTIONS_MENU),
            ("Algorithm Details", lambda: PATHFINDER_DETAILS_MENU),
            ("Back to Main Menu", lambda: WELCOME_MENU)
        ]
    )

def sorting_menu(window):
    return generic_menu(
        window,
        "Sorting Menu",
        [
            ("Launch Visualizer", lambda: sorting_main.launch_visualizer() or SORTING_MENU),
            ("Instructions", lambda: SORTING_INSTRUCTIONS_MENU),
            ("Algorithm Details", lambda: SORTING_DETAILS_MENU),
            ("Back to Main Menu", lambda: WELCOME_MENU)
        ]
    )

def pathfinder_details_menu(window):
    screen_width, screen_height = window.get_size()

    # Title
    title_font = pygame.font.SysFont('Verdana', 30, bold=True)
    title_text = title_font.render("Algorithm Details", True, COLORS['LIGHT_TEXT'])
    title_x, title_y = center_element(screen_width, title_text.get_width(), 30)

    # Description
    desc_font = pygame.font.SysFont('Verdana', 16)
    description_text = (
        "Pathfinding algorithms are essential for determining efficient routes between points in a grid. "
        "Widely used in navigation, robotics, and gaming, they enable smart decision-making and route optimization."
    )

    wrapped_lines = wrap_text(description_text, desc_font, screen_width - 200)
    total_text_height = len(wrapped_lines) * desc_font.get_height()
    description_y = title_y + title_text.get_height() + 20
    description_x = (screen_width - desc_font.size(max(wrapped_lines, key=len))[0]) // 2  # Center horizontally

    # Button and Text Settings
    section_gap = 30
    button_gap = 10
    button_width = 150
    button_height = 50

    button_font = pygame.font.SysFont('Verdana', 16)  # Smaller text for buttons

    # Sub-title
    sub_title_font = pygame.font.SysFont('Verdana', 20, bold=True)

    # Pathfinder Algorithms Section
    algos = ["A*", "Bi-A*", "BFS", "DFS", "GBFS", "JPS"]  # Define algos before using it
    pathfinder_section_y = description_y + total_text_height + section_gap
    pathfinder_section_title = sub_title_font.render("Pathfinding Algorithms", True, COLORS['LIGHT_TEXT'])
    pathfinder_section_x, pathfinder_section_y = center_element(screen_width, pathfinder_section_title.get_width(), pathfinder_section_y)

    algo_buttons_y_start = pathfinder_section_y + pathfinder_section_title.get_height() + button_gap

    # Define positions for the two rows
    row1_y = algo_buttons_y_start
    row2_y = algo_buttons_y_start + button_height + button_gap

    # Calculate starting X position to center the row of buttons horizontally
    algo_buttons_x_start = (screen_width - 3 * (button_width + button_gap)) // 2

    # Create buttons for two rows of three buttons each
    algo_buttons = [
        ButtonPrimary(algo_buttons_x_start + i * (button_width + button_gap), row1_y, button_width, button_height, algos[i], font=button_font)
        for i in range(3)
    ] + [
        ButtonPrimary(algo_buttons_x_start + i * (button_width + button_gap), row2_y, button_width, button_height, algos[i + 3], font=button_font)
        for i in range(3)
    ]

    # Update algo_buttons_y for the next section
    algo_buttons_y = row2_y + button_height

    # Heuristics Section
    heuristics = ["Manhattan", "Euclidean", "Diagonal", "Dijkstra"]  # Define heuristics before using it
    heuristics_section_y = algo_buttons_y + section_gap  # Adjust section gap here
    heuristics_section_title = sub_title_font.render("Heuristics", True, COLORS['LIGHT_TEXT'])
    heuristics_section_x, heuristics_section_y = center_element(screen_width, heuristics_section_title.get_width(), heuristics_section_y)

    heuristic_buttons_y = heuristics_section_y + heuristics_section_title.get_height() + button_gap
    heuristic_buttons_x_start = (screen_width - len(heuristics) * (button_width + button_gap)) // 2
    heuristic_buttons = [
        ButtonPrimary(heuristic_buttons_x_start + i * (button_width + button_gap), heuristic_buttons_y, button_width, button_height, heuristic, font=button_font)
        for i, heuristic in enumerate(heuristics)
    ]

    # Maze Generation Algorithms Section
    mazes = ["Recursive DFS", "Growing Tree", "Binary Tree", "Sidewinder"]  # Define the list of mazes
    maze_section_y = heuristic_buttons_y + button_height + section_gap
    maze_section_title = sub_title_font.render("Maze Generation Algorithms", True, COLORS['LIGHT_TEXT'])
    maze_section_x, maze_section_y = center_element(screen_width, maze_section_title.get_width(), maze_section_y)

    maze_buttons_y = maze_section_y + maze_section_title.get_height() + button_gap

    # Calculate starting X position to center the row of maze buttons horizontally
    maze_buttons_x_start = (screen_width - len(mazes) * (button_width + button_gap)) // 2

    maze_buttons = [
        ButtonPrimary(maze_buttons_x_start + i * (button_width + button_gap), maze_buttons_y, button_width, button_height, maze, font=button_font)
        for i, maze in enumerate(mazes)
    ]

    # 'Pathfinder' Button
    back_button_height = 60
    back_button_width = 300 + button_gap
    bold_button_font = pygame.font.SysFont('Verdana', 18, bold=True)
    back_button_y = maze_buttons_y + button_height  + section_gap
    back_button = ButtonPrimary(*center_element(screen_width, back_button_width + button_gap, back_button_y), back_button_width, back_button_height, "Pathfinder Menu", font=bold_button_font)

    buttons = algo_buttons + heuristic_buttons + maze_buttons + [back_button]

    # Drawing the Page
    window.fill(COLORS['DARK_GREEN'])
    window.blit(title_text, (title_x, title_y))
    
    for i, line in enumerate(wrapped_lines):
        line_surface = desc_font.render(line, True, COLORS['LIGHT_TEXT'])
        line_y = description_y + i * desc_font.get_height()
        window.blit(line_surface, (description_x, line_y))

    window.blit(pathfinder_section_title, (pathfinder_section_x, pathfinder_section_y))
    window.blit(heuristics_section_title, (heuristics_section_x, heuristics_section_y))
    window.blit(maze_section_title, (maze_section_x, maze_section_y))

    pygame.display.update()

    # Main loop to handle button interactions
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif back_button.is_clicked(event):
                return PATHFINDER_MENU

            # Handle clicks on specific algorithm buttons
            for button in algo_buttons + heuristic_buttons + maze_buttons:
                if button.is_clicked(event):
                    algo_name = button.text
                    
                    # Retrieve the algorithm info from the dictionary
                    algo_info = algorithms_info.get(algo_name, None)
                    
                    if algo_info:
                        title = algo_info.get("title", "Unknown")
                        short_description = algo_info.get("short_description", "No short description available.")
                        long_description = algo_info.get("long_description", ["No long description available."])
                        algo_type = algo_info.get("type", "Unknown")
                        time_complexity = algo_info.get("time_complexity", "Unknown")
                        space_complexity = algo_info.get("space_complexity", "Unknown")
                        common_applications = algo_info.get("common_applications", ["None specified"])
                        
                        # Return the details page with the unpacked information
                        return details_page(window, title, long_description, PATHFINDER_DETAILS_MENU, algo_type, time_complexity, space_complexity, common_applications)
                    else:
                        # Handle the case where the algorithm is not found in the dictionary
                        return details_page(window, "Unknown", ["No details available."], PATHFINDER_DETAILS_MENU)
                
        # Draw the buttons in each frame
        for button in buttons:
            button.draw(window)

        pygame.display.update()

def sorting_details_menu(window):
    screen_width, screen_height = window.get_size()

    # Title
    title_font = pygame.font.SysFont('Verdana', 30, bold=True)
    title_text = title_font.render("Algorithm Details", True, COLORS['LIGHT_TEXT'])
    title_x, title_y = center_element(screen_width, title_text.get_width(), 70)

    # Description
    desc_font = pygame.font.SysFont('Verdana', 16)
    description_text = (
        "Sorting algorithms are crucial for organizing data efficiently, whether it's numbers, names, or objects. From enhancing search performance to powering complex data analysis, they streamline processes and optimize operations in countless applications."
    )

    wrapped_lines = wrap_text(description_text, desc_font, screen_width - 200)
    total_text_height = len(wrapped_lines) * desc_font.get_height()
    description_y = title_y + title_text.get_height() + 20
    description_x = (screen_width - desc_font.size(max(wrapped_lines, key=len))[0]) // 2  # Center horizontally

    # Button and Text Settings
    section_gap = 50
    button_gap = 10
    button_width = 150
    button_height = 50

    button_font = pygame.font.SysFont('Verdana', 16)  # Smaller text for buttons

    # Sub-title
    sub_title_font = pygame.font.SysFont('Verdana', 20, bold=True)

    # Sorting Algorithms Section
    algos = [
        "Bubble Sort",
        "Insertion Sort",
        "Selection Sort",
        "Cocktail Shaker Sort",
        "Comb Sort",
        "Shell Sort",
        "Merge Sort",
        "Quick Sort",
        "Tim Sort",
        "Heap Sort",
        "Tree Sort",
        "Bogo Sort"
    ] 

    sorting_section_y = description_y + total_text_height + section_gap
    sorting_section_title = sub_title_font.render("Sorting Algorithms", True, COLORS['LIGHT_TEXT'])
    sorting_section_x, sorting_section_y = center_element(screen_width, sorting_section_title.get_width(), sorting_section_y)

    algo_buttons_y_start = sorting_section_y + sorting_section_title.get_height() + button_gap + 10

    # Define positions for the four rows
    row1_y = algo_buttons_y_start
    row2_y = algo_buttons_y_start + button_height + button_gap
    row3_y = algo_buttons_y_start + 2 * (button_height + button_gap)
    row4_y = algo_buttons_y_start + 3 * (button_height + button_gap)

    # Calculate starting X position to center the row of buttons horizontally (3 buttons per row)
    algo_buttons_x_start = (screen_width - 3 * (button_width + button_gap)) // 2

    # Create buttons for four rows of three buttons each
    algo_buttons = [
        ButtonPrimary(algo_buttons_x_start + i * (button_width + button_gap), row1_y, button_width, button_height, algos[i], font=button_font)
        for i in range(3)
    ] + [
        ButtonPrimary(algo_buttons_x_start + i * (button_width + button_gap), row2_y, button_width, button_height, algos[i + 3], font=button_font)
        for i in range(3)
    ] + [
        ButtonPrimary(algo_buttons_x_start + i * (button_width + button_gap), row3_y, button_width, button_height, algos[i + 6], font=button_font)
        for i in range(3)
    ] + [
        ButtonPrimary(algo_buttons_x_start + i * (button_width + button_gap), row4_y, button_width, button_height, algos[i + 9], font=button_font)
        for i in range(3)
    ]

    # Update algo_buttons_y for the next section if needed
    algo_buttons_y = row4_y + button_height


    # 'Sorting' Button
    back_button_height = 60
    back_button_width = 300 + button_gap
    bold_button_font = pygame.font.SysFont('Verdana', 18, bold=True)
    back_button_y = algo_buttons_y  + section_gap
    back_button = ButtonPrimary(*center_element(screen_width, back_button_width + button_gap, back_button_y), back_button_width, back_button_height, "Sorting Menu", font=bold_button_font)

    buttons = algo_buttons + [back_button]

    # Drawing the Page
    window.fill(COLORS['DARK_GREEN'])
    window.blit(title_text, (title_x, title_y))
    
    for i, line in enumerate(wrapped_lines):
        line_surface = desc_font.render(line, True, COLORS['LIGHT_TEXT'])
        line_y = description_y + i * desc_font.get_height()
        window.blit(line_surface, (description_x, line_y))

    window.blit(sorting_section_title, (sorting_section_x, sorting_section_y))

    pygame.display.update()

    # Main loop to handle button interactions
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif back_button.is_clicked(event):
                return SORTING_MENU

            # Handle clicks on specific algorithm buttons
            for button in algo_buttons:
                if button.is_clicked(event):
                    algo_name = button.text
                    
                    # Retrieve the algorithm info from the dictionary
                    algo_info = algorithms_info.get(algo_name, None)
                    
                    if algo_info:
                        title = algo_info.get("title", "Unknown")
                        short_description = algo_info.get("short_description", "No short description available.")
                        long_description = algo_info.get("long_description", ["No long description available."])
                        algo_type = algo_info.get("type", "Unknown")
                        time_complexity = algo_info.get("time_complexity", "Unknown")
                        space_complexity = algo_info.get("space_complexity", "Unknown")
                        common_applications = algo_info.get("common_applications", ["None specified"])
                        
                        # Return the details page with the unpacked information
                        return details_page(window, title, long_description, SORTING_DETAILS_MENU, algo_type, time_complexity, space_complexity, common_applications)
                    else:
                        # Handle the case where the algorithm is not found in the dictionary
                        return details_page(window, "Unknown", ["No details available."], SORTING_DETAILS_MENU)
                
        # Draw the buttons in each frame
        for button in buttons:
            button.draw(window)

        pygame.display.update()

# Function to display details about algorithms, heuristics, or mazes
def details_page(window, title, long_description, back_menu, algo_type=None, time_complexity=None, space_complexity=None, common_applications=None):
    screen_width, screen_height = window.get_size()

    # Define margins
    large_margin = 50  # Larger margin for time/space complexity
    small_margin = 50   # Smaller margin for long description and common applications

    # Clear the screen by filling it with a background color
    window.fill(COLORS['DARK_GREEN'])

    # Fonts
    title_font = pygame.font.SysFont('Verdana', 30, bold=True)
    info_font = pygame.font.SysFont('Verdana', 20)
    desc_font = pygame.font.SysFont('Verdana', 20)

    # Title and Type (Center the title)
    title_text = f"{title}"
    title_surface = title_font.render(title_text, True, COLORS['LIGHT_TEXT'])
    title_x, title_y = center_element(screen_width, title_surface.get_width(), 50)  # Keep centered
    window.blit(title_surface, (title_x, title_y))

    # Time Complexity (left-aligned with large margin)
    time_complexity_text = f"Time Complexity: {time_complexity if time_complexity else 'Unknown'}"
    time_complexity_surface = info_font.render(time_complexity_text, True, COLORS['LIGHT_TEXT'])
    time_complexity_y = title_y + title_surface.get_height() + 40
    window.blit(time_complexity_surface, (large_margin, time_complexity_y))

    # Space Complexity (left-aligned with large margin)
    space_complexity_text = f"Space Complexity: {space_complexity if space_complexity else 'Unknown'}"
    space_complexity_surface = info_font.render(space_complexity_text, True, COLORS['LIGHT_TEXT'])
    space_complexity_y = time_complexity_y + time_complexity_surface.get_height() + 20
    window.blit(space_complexity_surface, (large_margin, space_complexity_y))

    # Long Description (left-aligned with small margin)
    long_desc_start_y = space_complexity_y + space_complexity_surface.get_height() + 40
    description_y = long_desc_start_y
    wrapped_lines = [wrap_text(paragraph, desc_font, screen_width - small_margin * 2) for paragraph in long_description]

    # Draw the long description
    for paragraph_lines in wrapped_lines:
        for line in paragraph_lines:
            line_surface = desc_font.render(line, True, COLORS['LIGHT_TEXT'])
            window.blit(line_surface, (small_margin, description_y))
            description_y += desc_font.get_height()

        description_y += desc_font.get_height()  # Line break between paragraphs

    # Common Applications (left-aligned with small margin)
    applications_text = "Common Applications: " + ", ".join(common_applications) if common_applications else "Common Applications: None specified"
    applications_surface = info_font.render(applications_text, True, COLORS['LIGHT_TEXT'])
    applications_y = description_y + 20
    window.blit(applications_surface, (small_margin, applications_y))

    # Back Button (centered)
    back_button_y = applications_y + applications_surface.get_height() + 40
    back_button_width = 300
    back_button_height = 60
    back_button_x, back_button_y = center_element(screen_width, back_button_width, back_button_y)
    back_button_font = pygame.font.SysFont('Verdana', 18, bold=True)
    back_button = ButtonPrimary(back_button_x, back_button_y, back_button_width, back_button_height, "Back", font=back_button_font)

    buttons = [back_button]

    # Main loop to handle events and rendering
    while True:
        # Clear the screen before redrawing
        window.fill(COLORS['DARK_GREEN'])

        # Draw all elements
        window.blit(title_surface, (title_x, title_y))
        window.blit(time_complexity_surface, (large_margin, time_complexity_y))
        window.blit(space_complexity_surface, (large_margin, space_complexity_y))

        description_y = long_desc_start_y
        for paragraph_lines in wrapped_lines:
            for line in paragraph_lines:
                line_surface = desc_font.render(line, True, COLORS['LIGHT_TEXT'])
                window.blit(line_surface, (small_margin, description_y))
                description_y += desc_font.get_height()

            description_y += desc_font.get_height()  # Line break between paragraphs

        window.blit(applications_surface, (small_margin, applications_y))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif back_button.is_clicked(event):
                return back_menu

        # Draw the buttons
        for button in buttons:
            button.draw(window)

        pygame.display.update()

def pathfinding_instructions_menu(window):
    screen_width, screen_height = window.get_size()

    # Title
    title_font = pygame.font.SysFont('Verdana', 30, bold=True)
    title_text = title_font.render("Instructions", True, COLORS['LIGHT_TEXT'])
    title_x, title_y = center_element(screen_width, title_text.get_width(), 30)

    # Subsection fonts
    section_font = pygame.font.SysFont('Verdana', 24, bold=True)
    desc_font = pygame.font.SysFont('Verdana', 16)

    # Instructions content in subsections
    instructions = [
        {"section": "Cell Selection", "content": [
            "• Left click to select a cell, right click to reset a cell.",
            "• The first selected cell will be the start point.",
            "• The second selected cell will be the end point.",
            "• All other selected cells will act as barriers."
        ]},
        {"section": "Algorithm Selection", "content": [
            "• Choose a pathfinder algorithm, a heuristic, and a maze generation algorithm.",
            "• Each selected algorithm will display a short description."
        ]},
        {"section": "Execution", "content": [
            "• Press 'Start' to begin. If a path is found, the number of nodes and the path length will be displayed.",
            "• Use 'Clear Path' to remove the path and test different algorithms on the same layout.",
            "• Use 'Reset Maze' to reset the entire grid."
        ]}
    ]

    # Calculate Y position to center the instructions
    instructions_y = title_y + title_text.get_height() + 40
    max_text_width = screen_width - 150

    # Back Button
    back_button_y = screen_height - 200  # Position near the bottom
    back_button_width = 300
    back_button_height = 60
    back_button_x, back_button_y = center_element(screen_width, back_button_width, back_button_y)
    back_button_font = pygame.font.SysFont('Verdana', 18, bold=True)
    back_button = ButtonPrimary(back_button_x, back_button_y, back_button_width, back_button_height, "Pathfinder Menu", font=back_button_font)

    buttons = [back_button]

    # Main loop to handle button interactions and rendering
    while True:
        window.fill(COLORS['DARK_GREEN'])  # Clear screen with background color
        window.blit(title_text, (title_x, title_y))  # Render title

        # Render instructions
        instructions_y = title_y + title_text.get_height() + 40  # Reset starting Y position
        for section in instructions:
            # Render section title
            section_title_surface = section_font.render(section['section'], True, COLORS['LIGHT_TEXT'])
            window.blit(section_title_surface, ((screen_width - section_title_surface.get_width()) // 2, instructions_y))
            instructions_y += section_title_surface.get_height() + 10

            # Render content for each section
            for instruction in section['content']:
                wrapped_lines = wrap_text(instruction, desc_font, max_text_width)
                for line in wrapped_lines:
                    line_surface = desc_font.render(line, True, COLORS['LIGHT_TEXT'])
                    window.blit(line_surface, ((screen_width - max_text_width) // 2, instructions_y))
                    instructions_y += desc_font.get_height()

            instructions_y += desc_font.get_height() + 10 # Add some spacing between each section

        # Draw buttons
        for button in buttons:
            button.draw(window)

        pygame.display.update()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif back_button.is_clicked(event):
                return PATHFINDER_MENU

def sorting_instructions_menu(window):
    screen_width, screen_height = window.get_size()

    # Title
    title_font = pygame.font.SysFont('Verdana', 30, bold=True)
    title_text = title_font.render("Instructions", True, COLORS['LIGHT_TEXT'])
    title_x, title_y = center_element(screen_width, title_text.get_width(), 60)

    # Subsection fonts
    section_font = pygame.font.SysFont('Verdana', 24, bold=True)
    desc_font = pygame.font.SysFont('Verdana', 16)

    # Instructions content for sorting in subsections
    instructions = [
        {"section": "Setup", "content": [
            "• Select a sorting algorithm and choose the order (Ascending or Descending).",
            "• Adjust the array size and sorting speed using the sliders or buttons.",
        ]},
        {"section": "Execution", "content": [
            "• Press 'Start / Pause' to begin the sorting visualization and watch the algorithm in action.",
            "• Pause or resume the visualization at any time with the 'Start / Pause' button.",
        ]},
        {"section": "Reset & Step Mode", "content": [
            "• Use 'Reset Array' to create a new random array for sorting.",
            "• Activate 'Step Mode' to sort step by step, great for understanding how the algorithm works.",
            "• Press 'Step Forward' to move through the sorting process one operation at a time."
        ]}
    ]

    # Calculate Y position to center the instructions
    instructions_y = title_y + title_text.get_height() + 40
    max_text_width = screen_width - 150

    # Back Button
    back_button_y = screen_height - 200  # Position near the bottom
    back_button_width = 300
    back_button_height = 60
    back_button_x, back_button_y = center_element(screen_width, back_button_width, back_button_y)
    back_button_font = pygame.font.SysFont('Verdana', 18, bold=True)
    back_button = ButtonPrimary(back_button_x, back_button_y, back_button_width, back_button_height, "Sorting Menu", font=back_button_font)

    buttons = [back_button]

    # Main loop to handle button interactions and rendering
    while True:
        window.fill(COLORS['DARK_GREEN'])  # Clear screen with background color
        window.blit(title_text, (title_x, title_y))  # Render title

        # Render instructions
        instructions_y = title_y + title_text.get_height() + 40  # Reset starting Y position
        for section in instructions:
            # Render section title
            section_title_surface = section_font.render(section['section'], True, COLORS['LIGHT_TEXT'])
            window.blit(section_title_surface, ((screen_width - section_title_surface.get_width()) // 2, instructions_y))
            instructions_y += section_title_surface.get_height() + 10

            # Render content for each section
            for instruction in section['content']:
                wrapped_lines = wrap_text(instruction, desc_font, max_text_width)
                for line in wrapped_lines:
                    line_surface = desc_font.render(line, True, COLORS['LIGHT_TEXT'])
                    window.blit(line_surface, ((screen_width - max_text_width) // 2, instructions_y))
                    instructions_y += desc_font.get_height()

            instructions_y += desc_font.get_height() + 10 # Add some spacing between each section

        # Draw buttons
        for button in buttons:
            button.draw(window)

        pygame.display.update()  # Update the display

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif back_button.is_clicked(event):
                return SORTING_MENU



