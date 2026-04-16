import pygame, sys, math, json
from screens.homescreen import play, options
from screens.tutorial import *
from core.game_engine import Game
from components.button import Button
from components.textbox import TextBox
from core.config import *
from screens.character_selection import character_selection_screen, character_selected
from core.gamedata import gamedata, update_game_data


pygame.init()

# screen

SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Main Menu")

# load assets
bg = pygame.image.load("assets/Background4.png").convert()
LOGO = pygame.image.load("assets/Logo.png")
OUTLINE = pygame.image.load("assets/Outline.png")
OUTLINE = pygame.transform.scale(OUTLINE, (400, 300))
BOY = pygame.image.load("assets/boyslct.png")
GIRL = pygame.image.load("assets/girlslct.png")
bg_width = bg.get_width()
bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))
BUTTON1 = pygame.image.load("assets/Button1.png")
BUTTON2 = pygame.image.load("assets/Button2.png")

# scrolling variables
scroll = 0
tiles = math.ceil(WIN_WIDTH / bg_width) + 1


# font
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


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

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(
                        SCREEN,
                        tiles,
                        bg,
                        bg_width,
                        BOY,
                        GIRL,
                        OUTLINE,
                        BUTTON1,
                        BUTTON2,
                        Button,
                        get_font,
                        main_menu,
                    )
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options(
                        SCREEN,
                        tiles,
                        bg,
                        bg_width,
                        BOY,
                        GIRL,
                        OUTLINE,
                        BUTTON1,
                        BUTTON2,
                        Button,
                        get_font,
                        main_menu,
                    )
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


update_game_data()  # ensure game data is initialized

# run
main_menu()
