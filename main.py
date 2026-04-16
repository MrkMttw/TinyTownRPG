import pygame, sys, math, json
from core.shared import *
from screens.homescreen import play, options
from screens.battlefield import battlefield_screen
from screens.queue import queue_screen
from screens.tutorial import *
from core.game_engine import Game
from components.button import Button
from components.textbox import TextBox
from screens.character_selection import character_selection_screen, character_selected
from core.gamedata import gamedata, update_game_data

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
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # scrolling background
        for i in range(tiles):
            SCREEN.blit(bg, (i * bg_width + scroll, 0))

        scroll -= 1
        if abs(scroll) > bg_width:
            scroll = 0

        # logo
        LOGO_RECT = LOGO.get_rect(center=(640, 250))
        SCREEN.blit(LOGO, LOGO_RECT)

        # buttons
        PLAY_BUTTON = Button(
            image=BUTTON1,
            pos=(640, 450),
            text_input="PLAY",
            font=get_font(40),
            base_color="BLACK",
            hovering_color="#FFE14D",
        )

        OPTIONS_BUTTON = Button(
            image=BUTTON1,
            pos=(380, 510),
            text_input="OPTIONS",
            font=get_font(35),
            base_color="BLACK",
            hovering_color="#FFE14D",
        )

        QUIT_BUTTON = Button(
            image=BUTTON1,
            pos=(900, 510),
            text_input="QUIT",
            font=get_font(40),
            base_color="BLACK",
            hovering_color="#FFE14D",
        )

        BATTLE_BUTTON = Button(
            image=BUTTON1,
            pos=(640, 570),
            text_input="BATTLE",
            font=get_font(40),
            base_color="BLACK",
            hovering_color="#FFE14D",
        )

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, BATTLE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if BATTLE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    player_hp = 100
                    enemy_hp = 100
                    battle_ended = False
                    
                    while not battle_ended:
                        action_queue = queue_screen()
                        player_hp, enemy_hp, battle_ended = battlefield_screen(action_queue, player_hp, enemy_hp)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


update_game_data()  # ensure game data is initialized

# run
main_menu()
