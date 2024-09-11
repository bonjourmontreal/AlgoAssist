import pygame
from project import initialize_pygame, handle_events

def test_initialize_pygame():
    """Test if Pygame is initialized and screen is created."""
    screen = initialize_pygame()
    assert screen is not None, "Screen should be initialized."
    assert pygame.display.get_surface() is not None, "Pygame display surface should be initialized."

def test_handle_events_quit():
    """Test if QUIT event is handled properly."""
    screen = initialize_pygame()
    quit_event = pygame.event.Event(pygame.QUIT)  # Simulate QUIT event
    pygame.event.post(quit_event)
    assert handle_events(screen, "WELCOME_MENU") == False, "Handle events should return False on QUIT event."

def test_handle_events_no_quit():
    """Test if events other than QUIT are handled correctly."""
    screen = initialize_pygame()
    test_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE})  # Simulate a KEYDOWN event
    pygame.event.post(test_event)
    assert handle_events(screen, "WELCOME_MENU") == True, "Handle events should return True if no QUIT event."

