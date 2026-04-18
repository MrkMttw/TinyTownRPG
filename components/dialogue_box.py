import pygame
from core.config import WIN_WIDTH, WIN_HEIGHT
from core.shared import get_font


class DialogueBox:
    """Dialogue box for displaying NPC and player conversations
    
    Attributes:
        active: Whether the dialogue box is currently active
        dialogue_lines: List of dialogue lines to display
        current_line: Current line index being displayed
        speaker_name: Name of the speaker
        box_width: Width of the dialogue box
        box_height: Height of the dialogue box
        box_x: X position of the dialogue box
        box_y: Y position of the dialogue box
        text_margin: Margin around the text
        line_height: Height of each line
        chars_per_line: Maximum characters per line
        typing_speed: Speed of text typing animation
        typing_index: Current index in the typing animation
        typing_timer: Timer for typing animation
        display_text: Current text being displayed
    """
    
    def __init__(self):
        """
        Initialize the dialogue box
        
        Args:
            None
            
        Returns:
            None
        """
        self.active = False
        self.dialogue_lines = []
        self.current_line = 0
        self.speaker_name = ""
        self.box_width = 900
        self.box_height = 150
        self.box_x = (WIN_WIDTH - self.box_width) // 2
        self.box_y = WIN_HEIGHT - self.box_height - 20
        self.text_margin = 20
        self.line_height = 30
        self.chars_per_line = 50
        self.typing_speed = 2
        self.typing_index = 0
        self.typing_timer = 0
        self.display_text = ""
        
    def start_dialogue(self, speaker_name, dialogue_text):
        """
        Start a new dialogue
        
        Args:
            speaker_name: Name of the speaker
            dialogue_text: Text to display
            
        Returns:
            None
        """
        self.speaker_name = speaker_name
        self.dialogue_lines = self._wrap_text(dialogue_text)
        self.current_line = 0
        self.active = True
        self.typing_index = 0
        self.display_text = ""
        
    def _wrap_text(self, text):
        """
        Wrap text to fit in the dialogue box
        
        Args:
            text: Text to wrap
            
        Returns:
            List of wrapped lines
        """
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            # Check if adding the word would exceed the character limit
            if len(current_line + " " + word) <= self.chars_per_line:
                current_line += " " + word if current_line else word
            else:
                # Add the current line to the list and start a new line
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            # Add the last line to the list
            lines.append(current_line)

        # Return the list of wrapped lines
        return lines
    
    def handle_input(self, event):
        """Handle keyboard input for dialogue
        Args:
            event: Pygame event to handle
            
        Returns:
            str: "battle" if F key pressed and dialogue complete, "back" if any other key pressed, False otherwise
        """
        if not self.active:
            # If dialogue is not active, return False
            return False
            
        if event.type == pygame.KEYDOWN:
            # Check if dialogue is complete
            if self.current_line >= len(self.dialogue_lines):
                if event.key == pygame.K_f:
                    self.active = False
                    return "battle"
                else:
                    # Any other key closes the dialogue
                    self.active = False
                    return "back"
            
            # Dialogue still in progress
            if event.key == pygame.K_f or event.key == pygame.K_SPACE:
                if self.typing_index < len(self.dialogue_lines[self.current_line]):
                    # Skip typing animation
                    self.typing_index = len(self.dialogue_lines[self.current_line])
                    self.display_text = self.dialogue_lines[self.current_line]
                else:
                    # Advance to next line
                    self.current_line += 1
                    if self.current_line >= len(self.dialogue_lines):
                        # Dialogue complete
                        pass
                    else:
                        self.typing_index = 0
                        self.display_text = ""
            elif event.key == pygame.K_ESCAPE:
                # ESC key closes the dialogue
                self.active = False
                return "back"
                
        return None
    
    def update(self):
        """
        Update typing animation
        
        Args:
            None
            
        Returns:
            None
        """
        if self.active and self.current_line < len(self.dialogue_lines):
            # If dialogue is active and not at the end of the dialogue
            current_line_text = self.dialogue_lines[self.current_line]
            if self.typing_index < len(current_line_text):
                # If the current line is not fully displayed, continue typing
                self.typing_timer += 1
                if self.typing_timer >= self.typing_speed:
                    # If the typing timer is greater than or equal to the typing speed, add a character
                    self.typing_index += 1
                    self.display_text = current_line_text[:self.typing_index]
                    self.typing_timer = 0
            else:
                # If the current line is fully displayed, show it
                self.display_text = current_line_text
    
    def draw(self, surface):
        """
        Draw the dialogue box
        
        Args:
            surface: Pygame surface to draw on
            
        Returns:
            None
        """
        if not self.active:
            return
            
        # Draw semi-transparent background
        box_surface = pygame.Surface((self.box_width, self.box_height))
        box_surface.set_alpha(230)
        box_surface.fill((30, 30, 50))
        surface.blit(box_surface, (self.box_x, self.box_y))
        
        # Draw border
        pygame.draw.rect(surface, (100, 100, 150), 
                        (self.box_x, self.box_y, self.box_width, self.box_height), 3)
        
        # Draw speaker name
        if self.speaker_name:
            name_font = get_font(24)
            name_text = name_font.render(self.speaker_name, True, (255, 200, 100))
            name_rect = name_text.get_rect()
            name_rect.topleft = (self.box_x + self.text_margin, self.box_y + 10)
            surface.blit(name_text, name_rect)
            
            # Draw separator line
            pygame.draw.line(surface, (100, 100, 150),
                           (self.box_x + self.text_margin, self.box_y + 40),
                           (self.box_x + self.box_width - self.text_margin, self.box_y + 40), 2)
        
        # Draw dialogue text
        text_font = get_font(20)
        text_y = self.box_y + 55
        
        if self.current_line < len(self.dialogue_lines):
            # If there are more lines to display, draw the current line
            text_surface = text_font.render(self.display_text, True, (255, 255, 255))
            surface.blit(text_surface, (self.box_x + self.text_margin, text_y))
        
        # Draw continue indicator
        if self.current_line < len(self.dialogue_lines):
            # If there are more lines to display, draw the continue indicator
            if self.typing_index >= len(self.dialogue_lines[self.current_line]):
                # If the current line is fully displayed, show the continue indicator
                indicator_font = get_font(16)
                indicator_text = indicator_font.render("Press F to continue", True, (200, 200, 200))
                indicator_rect = indicator_text.get_rect()
                indicator_rect.bottomright = (self.box_x + self.box_width - 10, self.box_y + self.box_height - 10)
                surface.blit(indicator_text, indicator_rect)
        else:
            # Dialogue complete - show battle and go back options
            indicator_font = get_font(16)
            indicator_text = indicator_font.render("Press F to battle | Any key to go back", True, (200, 200, 200))
            indicator_rect = indicator_text.get_rect()
            indicator_rect.bottomright = (self.box_x + self.box_width - 10, self.box_y + self.box_height - 10)
            surface.blit(indicator_text, indicator_rect)
