import pygame
from core.config import WIN_WIDTH, WIN_HEIGHT
from core.shared import get_font


class DialogueBox:
    """Dialogue box for displaying NPC and player conversations"""
    
    def __init__(self):
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
        """Start a new dialogue"""
        self.speaker_name = speaker_name
        self.dialogue_lines = self._wrap_text(dialogue_text)
        self.current_line = 0
        self.active = True
        self.typing_index = 0
        self.display_text = ""
        
    def _wrap_text(self, text):
        """Wrap text to fit in the dialogue box"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line + " " + word) <= self.chars_per_line:
                current_line += " " + word if current_line else word
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
            
        return lines
    
    def handle_input(self, event):
        """Handle keyboard input for dialogue"""
        if not self.active:
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
                self.active = False
                return "back"
                
        return None
    
    def update(self):
        """Update typing animation"""
        if self.active and self.current_line < len(self.dialogue_lines):
            current_line_text = self.dialogue_lines[self.current_line]
            if self.typing_index < len(current_line_text):
                self.typing_timer += 1
                if self.typing_timer >= self.typing_speed:
                    self.typing_index += 1
                    self.display_text = current_line_text[:self.typing_index]
                    self.typing_timer = 0
            else:
                self.display_text = current_line_text
    
    def draw(self, surface):
        """Draw the dialogue box"""
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
            text_surface = text_font.render(self.display_text, True, (255, 255, 255))
            surface.blit(text_surface, (self.box_x + self.text_margin, text_y))
        
        # Draw continue indicator
        if self.current_line < len(self.dialogue_lines):
            if self.typing_index >= len(self.dialogue_lines[self.current_line]):
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
