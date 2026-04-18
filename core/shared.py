import pygame
import math
from core.config import WIN_WIDTH, WIN_HEIGHT

pygame.init()

# Set up the display
SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Tiny Town")

# Load assets
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

# Scrolling variables
tiles = math.ceil(WIN_WIDTH / bg_width) + 1


def get_font(size):
    # Get font from assets
    return pygame.font.Font("assets/font.ttf", size)

"""
Shared variables and functions for the game
"""