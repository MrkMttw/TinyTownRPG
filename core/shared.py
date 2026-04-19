import pygame
import math
from core.config import WIN_WIDTH, WIN_HEIGHT, SETTINGS

pygame.init()

# Initialize mixer for audio
pygame.mixer.init()

# Load background music from settings
bgm_path = SETTINGS.get("BGM_PATH", "assets/esefex/bg_sfx.mp3")
pygame.mixer.music.load(bgm_path)

# Play background music if enabled
if SETTINGS["BGM_ENABLED"]:
    pygame.mixer.music.set_volume(SETTINGS["BGM_VOLUME"])
    pygame.mixer.music.play(-1)

def update_audio_settings():
    """Update audio settings based on current SETTINGS"""
    if SETTINGS["BGM_ENABLED"]:
        pygame.mixer.music.set_volume(SETTINGS["BGM_VOLUME"])
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

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
BOY_PANEL = pygame.image.load("assets/cutscenes/boy_panel.png")
GIRL_PANEL = pygame.image.load("assets/cutscenes/girl_panel.png")

# Scrolling variables
tiles = math.ceil(WIN_WIDTH / bg_width) + 1


def get_font(size):
    # Get font from assets
    return pygame.font.Font("assets/font.ttf", size)

"""
Shared variables and functions for the game
"""