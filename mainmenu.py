import pygame, sys, math
from main import Game
from button import Button
from config import *

pygame.init()

# screen

SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Main Menu")

# load assets
bg = pygame.image.load("assets/Background4.png").convert()
LOGO = pygame.image.load("assets/Logo.png")

bg_width = bg.get_width()
bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))

# scrolling variables
scroll = 0
tiles = math.ceil(WIN_WIDTH / bg_width) + 1

# font
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# ================= PLAY =================
def play():
    game = Game(SCREEN)
    game.new()

    while game.playing:
        game.events()
        game.update()
        game.draw()

    pygame.event.clear()  # prevent input bugs
    return
    
# ================= OPTIONS =================
def options():
    global scroll
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        # scrolling background
        for i in range(tiles):
            SCREEN.blit(bg, (i * bg_width + scroll, 0))

        scroll -= 1
        if abs(scroll) > bg_width:
            scroll = 0

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 500), 
                              text_input="BACK", font=get_font(60), 
                              base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return  # go back

        pygame.display.update()

# ================= MAIN MENU =================
def main_menu():
    global scroll
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # 🔥 scrolling background
        for i in range(tiles):
            SCREEN.blit(bg, (i * bg_width + scroll, 0))

        scroll -= 2
        if abs(scroll) > bg_width:
            scroll = 0

        # 🖼️ logo
        LOGO_RECT = LOGO.get_rect(center=(640, 250))
        SCREEN.blit(LOGO, LOGO_RECT)

        # 🎮 buttons
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Button1.png"), pos=(640, 450), 
                             text_input="PLAY", font=get_font(40), 
                             base_color="White", hovering_color="#FFE14D")

        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Button1.png"), pos=(380, 510), 
                                text_input="OPTIONS", font=get_font(35), 
                                base_color="White", hovering_color="#FFE14D")

        QUIT_BUTTON = Button(image=pygame.image.load("assets/Button1.png"), pos=(900, 510), 
                             text_input="QUIT", font=get_font(40), 
                             base_color="White", hovering_color="#FFE14D")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
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
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# run
main_menu()