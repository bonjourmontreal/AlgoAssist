import pygame

# Color Palette for UI, Pathfinder App and Sorting App
COLORS = {
    # UI COLORS
    "DARK_GREEN": (18, 55, 42),        
    "MEDIUM_GREEN": (67, 104, 80),      
    "LIGHT_GREEN": (173, 188, 159),     
    "LIGHTER_GREEN": (219, 231, 201),
    "LIGHT_CREAM": (251, 250, 218),

    "DARK_TEXT": (18, 55, 42), 
    "LIGHT_TEXT": (251, 250, 218),

    # Pathfinder / Sorting COLORS
    "RED": (255, 102, 102),        # Lighter Red
    "GREEN": (102, 255, 102),      # Lighter Green
    "BLUE": (102, 178, 255),       # Lighter Blue
    "YELLOW": (255, 255, 153),     # Lighter Yellow
    "WHITE": (255, 255, 255),      # White (remains the same)
    "BLACK": (77, 77, 77),         # Soft Black / Dark Grey
    "PURPLE": (204, 153, 255),     # Lighter Purple
    "ORANGE": (255, 178, 102),     # Lighter Orange
    "GREY": (192, 192, 192),       # Light Grey
    "TURQUOISE": (153, 255, 255),  # Lighter Turquoise
    "PINK": (255, 204, 229),       # Lighter Pink
}

class Button:
    def __init__(self, drawn_x, drawn_y, width, height, text, font, button_color, hover_button_color,
                 hovered_x=None, hovered_y=None, text_color=COLORS['DARK_TEXT'], hover_text_color=COLORS['LIGHT_TEXT'],
                 border_color=None, hover_border_color=None):
        # Drawing coordinates (where the button is drawn)
        self.drawn_rect = pygame.Rect(drawn_x, drawn_y, width, height)

        # Hover coordinates (where the button detects hover)
        self.hovered_x = hovered_x if hovered_x is not None else drawn_x
        self.hovered_y = hovered_y if hovered_y is not None else drawn_y
        self.hover_rect = pygame.Rect(self.hovered_x, self.hovered_y, width, height)

        # Button properties
        self.text = text
        self.font = font
        self.button_color = button_color
        self.hover_button_color = hover_button_color
        self.text_color = text_color
        self.hover_text_color = hover_text_color if hover_text_color else text_color
        self.border_color = border_color if border_color else text_color
        self.hover_border_color = hover_border_color if hover_border_color else border_color

    def draw(self, window):
        # Change the button color, text color, and border color if hovered
        current_button_color = self.hover_button_color if self.is_hovered() else self.button_color
        current_text_color = self.hover_text_color if self.is_hovered() else self.text_color
        current_border_color = self.hover_border_color if self.is_hovered() else self.border_color

        # Draw the button rectangle with the current button color
        pygame.draw.rect(window, current_button_color, self.drawn_rect)

        # Draw the border with the current border color
        pygame.draw.rect(window, current_border_color, self.drawn_rect, 3)

        # Measure text width
        text_surface = self.font.render(self.text, True, current_text_color)
        text_width, text_height = text_surface.get_size()

        # Check if text is too wide for the button, then wrap or reduce font size
        if text_width > self.drawn_rect.width - 10:  # Add padding margin
            wrapped_text = wrap_text(self.text, self.font, self.drawn_rect.width - 10)
            self.render_wrapped_text(window, wrapped_text, current_text_color)
        else:
            # Render the text with the current text color
            text_rect = text_surface.get_rect(center=self.drawn_rect.center)
            window.blit(text_surface, text_rect)

    def render_wrapped_text(self, window, wrapped_text, text_color):
        # Total number of lines to render
        max_lines = len(wrapped_text)

        # Adjust font size if too many lines (optional, based on requirement)
        if max_lines > 2:  # If more than two lines, shrink the text
            self.font = pygame.font.SysFont('Verdana', 10)  # Adjust font size as needed

        # Calculate the total height of the block of text (all lines combined)
        total_text_height = max_lines * self.font.get_height()

        # Calculate the starting y position to center the entire block vertically in the button
        # We calculate this based on the total height of the text block and the button height
        start_y = self.drawn_rect.centery - total_text_height // 3

        # Render each line, adjusting for each line's height
        for i, line in enumerate(wrapped_text):
            text_surface = self.font.render(line, True, text_color)
            text_rect = text_surface.get_rect(center=(self.drawn_rect.centerx, start_y + i * self.font.get_height()))
            window.blit(text_surface, text_rect)

    def is_hovered(self):
        return self.hover_rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONUP and self.is_hovered():
            return True
        return False
    
class ButtonPrimary(Button):
    def __init__(self, drawn_x, drawn_y, width, height, text, font=None, button_color=None, hover_button_color=None, 
                 hovered_x=None, hovered_y=None, text_color=None, hover_text_color=None, border_color=None, hover_border_color=None):
        # Define default styles for the primary button
        default_font = font or pygame.font.SysFont('Verdana', 40)
        default_button_color = button_color or COLORS['LIGHT_GREEN']
        default_hover_button_color = hover_button_color or COLORS['MEDIUM_GREEN']
        default_text_color = text_color or COLORS['DARK_TEXT']
        default_hover_text_color = hover_text_color or COLORS['LIGHT_TEXT']
        default_border_color = border_color or COLORS['LIGHT_CREAM']
        default_hover_border_color = hover_border_color or COLORS['LIGHTER_GREEN']
        
        # Call the parent constructor with the defaults or provided values
        super().__init__(
            drawn_x, drawn_y, width, height, text, 
            default_font, 
            default_button_color, 
            default_hover_button_color, 
            hovered_x=hovered_x, hovered_y=hovered_y,
            text_color=default_text_color, 
            hover_text_color=default_hover_text_color, 
            border_color=default_border_color, 
            hover_border_color=default_hover_border_color
        )

    def update_text(self, new_text):
        """Updates the button's text."""
        self.text = new_text  # Update the button's text

def draw_text(window, font, text, color, y, max_width=None, center_x=None):
    """Helper function to render and draw text with optional wrapping and centering."""
    if max_width:
        lines = wrap_text(text, font, max_width)
        max_line_width = max(font.size(line)[0] for line in lines)
        x = center_x - (max_line_width // 2) if center_x else 0
        for i, line in enumerate(lines):
            line_surface = font.render(line, True, color)
            window.blit(line_surface, (x, y + i * font.get_height()))
    else:
        line_surface = font.render(text, True, color)
        window.blit(line_surface, (center_x - line_surface.get_width() // 2, y))

def wrap_text(text, font, max_width):
    """Splits text into lines that fit within the specified max_width."""
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    
    lines.append(current_line)  # Add the last line
    return lines

def center_element(screen_width, element_width, y_offset):
    """Calculate position to center an element horizontally on the screen."""
    x = (screen_width - element_width) // 2  # Center the element horizontally
    y = y_offset
    return x, y
