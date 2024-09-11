import pygame
from pages import *

WINDOW_WIDTH, WINDOW_HEIGHT = 1060, 720

def main():
    """Main function to run the AlgoAssist program."""
    screen = initialize_pygame()
    current_menu = WELCOME_MENU
    running = True

    while running:
        current_menu = switch_menu(current_menu, screen)
        handle_events(screen, current_menu)
        pygame.display.update()

    pygame.quit()

def initialize_pygame():
    """Initializes pygame and sets up the display window."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("AlgoAssist")
    return screen

def switch_menu(current_menu, screen):
    """Switches between different menus based on user input."""
    if current_menu == WELCOME_MENU:
        return main_menu(screen)
    elif current_menu == PATHFINDER_MENU:
        return pathfinder_menu(screen)
    elif current_menu == SORTING_MENU:
        return sorting_menu(screen)
    elif current_menu == PATHFINDER_DETAILS_MENU:
        return pathfinder_details_menu(screen)
    elif current_menu == PATHFINDER_INSTRUCTIONS_MENU:
        return pathfinding_instructions_menu(screen)
    elif current_menu == SORTING_DETAILS_MENU:
        return sorting_details_menu(screen)
    elif current_menu == SORTING_INSTRUCTIONS_MENU:
        return sorting_instructions_menu(screen)
    else:
        return WELCOME_MENU

def handle_events(screen, current_menu):
    """Handles events for the current menu."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

if __name__ == "__main__":
    main()