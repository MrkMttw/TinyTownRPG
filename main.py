import pygame, sys
from core.shared import *
from screens.homescreen import play
from screens.settings import show_settings
from screens.tutorial import *
from components.button import Button
from core.gamedata import update_game_data

pygame.init()

# scrolling variables
scroll = 0


# ================= MAIN MENU =================
def main_menu():
    """
    Main menu of the game

    Attributes:
        scroll: scroll position
        MENU_MOUSE_POS: mouse position
        PLAY_BUTTON: play button
        OPTIONS_BUTTON: options button
        QUIT_BUTTON: quit button
        BATTLE_BUTTON: battle button
    Parameters:
        None
    """
    global scroll
    while True:
        """
        Get mouse position and update background scroll
        """
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # scrolling background
        scroll = draw_scrolling_bg(scroll, 1)

        # logo
        LOGO_RECT = LOGO.get_rect(center=(640, 250))
        SCREEN.blit(LOGO, LOGO_RECT)

        # Play button
        PLAY_BUTTON = Button(
            image=BUTTON1,
            pos=(640, 450),
            text_input="PLAY",
            font=get_font(40),
            base_color="BLACK",
            hovering_color="#FFE14D",
        )

        # Options button
        OPTIONS_BUTTON = Button(
            image=BUTTON1,
            pos=(380, 510),
            text_input="SETTINGS",
            font=get_font(35),
            base_color="BLACK",
            hovering_color="#FFE14D",
        )

        # Quit button
        QUIT_BUTTON = Button(
            image=BUTTON1,
            pos=(900, 510),
            text_input="QUIT",
            font=get_font(40),
            base_color="BLACK",
            hovering_color="#FFE14D",
        )

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            # Check if button is hovered and update it
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            # Handle quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle mouse button down event
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Start the game
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Show settings
                    show_settings()
                    
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # Quit the game
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


# Initialize game data
update_game_data()

# Run the game
main_menu()
