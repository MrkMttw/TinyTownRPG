"""
Settings screen for audio and display options
"""
import pygame
import sys
import math
from core.config import (
    SETTINGS, WIN_WIDTH, WIN_HEIGHT, save_settings
)
from core.shared import SCREEN, get_font, update_audio_settings
from components.button import Button
from screens.character_selection import character_selection_screen
from core.gamedata import gamedata, update_game_data


class SettingsScreen:
    """Settings screen with audio and display controls
    
    Attributes:
        sfx_enabled: Boolean for sound effects toggle
        sfx_volume: Float for sound effects volume (0.0-1.0)
        bgm_enabled: Boolean for background music toggle
        bgm_volume: Float for background music volume (0.0-1.0)
        fullscreen: Boolean for fullscreen mode
    """

    def __init__(self):
        """Initialize settings with current config values"""
        self.sfx_enabled = SETTINGS["SFX_ENABLED"]
        self.sfx_volume = SETTINGS["SFX_VOLUME"]
        self.bgm_enabled = SETTINGS["BGM_ENABLED"]
        self.bgm_volume = SETTINGS["BGM_VOLUME"]
        self.fullscreen = SETTINGS["FULLSCREEN"]
        
        # Load background image for scrolling (same approach as character_selection)
        try:
            self.bg = pygame.image.load("assets/Background4.png").convert()
            self.bg_width = self.bg.get_width()
            self.bg = pygame.transform.scale(self.bg, (WIN_WIDTH, WIN_HEIGHT))
            self.tiles = math.ceil(WIN_WIDTH / self.bg_width) + 1
            self.scroll = 0
        except pygame.error as e:
            print(f"Error loading background: {e}")
            self.bg = None

    def draw_slider(self, screen, x, y, width, height, value, label):
        """Draw a volume slider
        
        Args:
            screen: Pygame screen surface
            x: X position
            y: Y position
            width: Slider width
            height: Slider height
            value: Current volume value (0.0-1.0)
            label: Label text
            
        Returns:
            Pygame rect for the slider handle
        """
        # Draw label
        label_text = get_font(24).render(f"{label}: {int(value * 100)}%", True, (255, 255, 255))
        screen.blit(label_text, (x, y - 30))

        # Draw slider background
        slider_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, (100, 100, 100), slider_rect)
        pygame.draw.rect(screen, (150, 150, 150), slider_rect, 2)

        # Draw slider handle
        handle_x = x + (value * width)
        handle_rect = pygame.Rect(handle_x - 10, y - 5, 20, height + 10)
        pygame.draw.rect(screen, (255, 255, 255), handle_rect)

        return handle_rect

    def draw_toggle(self, screen, x, y, enabled, label):
        """Draw a toggle button for on/off settings
        
        Args:
            screen: Pygame screen surface
            x: X position (leftmost position)
            y: Y position
            enabled: Boolean current state
            label: Label text
            
        Returns:
            Pygame rect for the toggle button
        """
        # Draw label
        label_text = get_font(24).render(label, True, (255, 255, 255))
        screen.blit(label_text, (x, y))

        # Draw toggle button to the right of the label, vertically centered
        text_height = label_text.get_height()
        toggle_y = y + (text_height - 40) // 2
        toggle_rect = pygame.Rect(x + label_text.get_width() + 20, toggle_y, 60, 30)
        color = (0, 200, 0) if enabled else (200, 0, 0)
        pygame.draw.rect(screen, color, toggle_rect)
        pygame.draw.rect(screen, (255, 255, 255), toggle_rect, 2)

        # Draw toggle text
        toggle_text = get_font(20).render("ON" if enabled else "OFF", True, (255, 255, 255))
        toggle_text_rect = toggle_text.get_rect(center=toggle_rect.center)
        screen.blit(toggle_text, toggle_text_rect)

        return toggle_rect

    def apply_settings(self):
        """Apply settings to the game"""
        # Check if fullscreen changed before saving
        fullscreen_changed = self.fullscreen != SETTINGS["FULLSCREEN"]
        
        # Save settings to config file
        save_settings(
            self.sfx_enabled,
            self.sfx_volume,
            self.bgm_enabled,
            self.bgm_volume,
            self.fullscreen
        )

        # Update audio settings dynamically
        update_audio_settings()

        # Update fullscreen
        if fullscreen_changed:
            if self.fullscreen:
                SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.FULLSCREEN)
            else:
                SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    def run(self):
        """Run the settings screen loop
        
        Returns:
            None when settings are saved and screen is exited
        """
        running = True
        dragging_sfx = False
        dragging_bgm = False

        while running:
            SETTINGS_MOUSE_POS = pygame.mouse.get_pos()

            # Scrolling background logic (same as character_selection)
            if self.bg:
                for i in range(self.tiles):
                    SCREEN.blit(self.bg, (i * self.bg_width + self.scroll, 0))

                self.scroll -= 1.2
                if abs(self.scroll) > self.bg_width:
                    # Reset scroll when image repeats
                    self.scroll = 0
            else:
                # Fallback to solid color
                SCREEN.fill((30, 30, 30))

            # Draw title
            title_text = get_font(50).render("SETTINGS", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(WIN_WIDTH // 2, 80))
            SCREEN.blit(title_text, title_rect)

            # Draw SFX toggle
            sfx_toggle_rect = self.draw_toggle(
                SCREEN, WIN_WIDTH // 2 - 150, 160, self.sfx_enabled, "Sound Effects"
            )

            # Draw SFX volume slider
            sfx_slider_rect = self.draw_slider(
                SCREEN, WIN_WIDTH // 2 - 150, 230, 300, 20, self.sfx_volume, "SFX Volume"
            )

            # Draw BGM toggle
            bgm_toggle_rect = self.draw_toggle(
                SCREEN, WIN_WIDTH // 2 - 150, 280, self.bgm_enabled, "Background Music"
            )

            # Draw BGM volume slider
            bgm_slider_rect = self.draw_slider(
                SCREEN, WIN_WIDTH // 2 - 150, 350, 300, 20, self.bgm_volume, "BGM Volume"
            )

            # Draw fullscreen toggle
            fullscreen_toggle_rect = self.draw_toggle(
                SCREEN, WIN_WIDTH // 2 - 150, 400, self.fullscreen, "Fullscreen Mode"
            )

            # Draw back button
            BACK_BUTTON = Button(
                image=None,
                pos=(WIN_WIDTH // 2, 550),
                text_input="BACK",
                font=get_font(30),
                base_color="WHITE",
                hovering_color="#FFE14D",
            )
            BACK_BUTTON.changeColor(SETTINGS_MOUSE_POS)
            BACK_BUTTON.update(SCREEN)

            # Draw next button (no border, bottom right)
            NEXT_BUTTON = Button(
                image=None,
                pos=(WIN_WIDTH - 100, WIN_HEIGHT - 50),
                text_input="NEXT",
                font=get_font(30),
                base_color="WHITE",
                hovering_color="#FFE14D",
            )
            NEXT_BUTTON.changeColor(SETTINGS_MOUSE_POS)
            NEXT_BUTTON.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                        self.apply_settings()
                        return

                    if NEXT_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                        self.apply_settings()
                        # Navigate to character selection screen with proper callbacks
                        def on_character_selected(char_id):
                            """Update character in gamedata and save to JSON"""
                            gamedata["in_game_data"][0]["CHARACTER"] = char_id
                            update_game_data()
                        
                        def on_back():
                            """Return to settings screen (no action needed)"""
                            pass
                        
                        character_selection_screen(
                            on_select_callback=on_character_selected,
                            back_callback=on_back
                        )
                        return

                    # Handle SFX toggle
                    if sfx_toggle_rect.collidepoint(event.pos):
                        self.sfx_enabled = not self.sfx_enabled

                    # Handle BGM toggle
                    if bgm_toggle_rect.collidepoint(event.pos):
                        self.bgm_enabled = not self.bgm_enabled

                    # Handle fullscreen toggle
                    if fullscreen_toggle_rect.collidepoint(event.pos):
                        self.fullscreen = not self.fullscreen

                    # Handle slider dragging
                    if sfx_slider_rect.collidepoint(event.pos):
                        dragging_sfx = True
                    if bgm_slider_rect.collidepoint(event.pos):
                        dragging_bgm = True

                if event.type == pygame.MOUSEBUTTONUP:
                    dragging_sfx = False
                    dragging_bgm = False

                if event.type == pygame.MOUSEMOTION:
                    if dragging_sfx:
                        mouse_x = event.pos[0]
                        slider_x = WIN_WIDTH // 2 - 150
                        slider_width = 300
                        new_value = (mouse_x - slider_x) / slider_width
                        self.sfx_volume = max(0.0, min(1.0, new_value))

                    if dragging_bgm:
                        mouse_x = event.pos[0]
                        slider_x = WIN_WIDTH // 2 - 150
                        slider_width = 300
                        new_value = (mouse_x - slider_x) / slider_width
                        self.bgm_volume = max(0.0, min(1.0, new_value))

            pygame.display.update()


def show_settings():
    """Settings screen function"""
    settings_screen = SettingsScreen()
    settings_screen.run()
