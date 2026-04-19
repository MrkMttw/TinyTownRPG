"""
Settings screen for audio and display options
"""
import pygame
import sys
import math
from core.config import (
    SETTINGS, WIN_WIDTH, WIN_HEIGHT, save_settings
)
from core.shared import SCREEN, get_font, update_audio_settings, draw_scrolling_bg
from components.button import Button
from components.ui_widgets import draw_slider, draw_toggle
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
        
        self.scroll = 0


    def apply_settings(self):
        """Apply settings to the game"""
        global SCREEN
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

            # Scrolling background logic
            self.scroll = draw_scrolling_bg(self.scroll, 1.2)

            # Draw title
            title_text = get_font(50).render("SETTINGS", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(WIN_WIDTH // 2, 80))
            SCREEN.blit(title_text, title_rect)

            # Draw SFX toggle
            sfx_toggle_rect = draw_toggle(
                SCREEN, WIN_WIDTH // 2 - 150, 160, self.sfx_enabled, "Sound Effects"
            )

            # Draw SFX volume slider
            sfx_slider_rect = draw_slider(
                SCREEN, WIN_WIDTH // 2 - 150, 230, 300, 20, self.sfx_volume, "SFX Volume"
            )

            # Draw BGM toggle
            bgm_toggle_rect = draw_toggle(
                SCREEN, WIN_WIDTH // 2 - 150, 280, self.bgm_enabled, "Background Music"
            )

            # Draw BGM volume slider
            bgm_slider_rect = draw_slider(
                SCREEN, WIN_WIDTH // 2 - 150, 350, 300, 20, self.bgm_volume, "BGM Volume"
            )

            # Draw fullscreen toggle
            fullscreen_toggle_rect = draw_toggle(
                SCREEN, WIN_WIDTH // 2 - 150, 400, self.fullscreen, "Fullscreen Mode"
            )

            # Draw back button
            BACK_BUTTON = Button(
                image=None,
                pos=(WIN_WIDTH // 2, 550),
                text_input="SAVE",
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
