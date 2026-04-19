"""
Pause menu component for the game
"""
import pygame
import sys
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font
from screens.settings import show_settings


class PauseMenu:
    """Pause menu class with continue and quit options
    
    Attributes:
        active: Boolean indicating if pause menu is active
    """

    def __init__(self):
        """Initialize the pause menu"""
        self.active = False


    def toggle(self):
        """Toggle pause menu on/off"""
        self.active = not self.active

    def update(self):
        """Update pause menu state (placeholder for future updates)"""
        pass

    def handle_events(self):
        """Handle pause menu events
        
        Returns:
            "continue" if F pressed, "quit" if Q pressed
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.toggle()
                    return "continue"
                if event.key == pygame.K_f:
                    self.toggle()
                    return "continue"
                if event.key == pygame.K_q:
                    self.toggle()
                    return "quit"

        return None


    def draw(self, screen):
        """Draw pause menu overlay
        
        Args:
            screen: Pygame screen surface
        """
        # Create semi-transparent overlay
        overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Draw pause title
        pause_text = get_font(60).render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 150))
        screen.blit(pause_text, pause_rect)

        # Draw instructions
        continue_text = get_font(40).render("Press F to Continue", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 30))
        screen.blit(continue_text, continue_rect)

        quit_text = get_font(40).render("Press Q to Quit", True, (255, 255, 255))
        quit_rect = quit_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50))
        screen.blit(quit_text, quit_rect)
