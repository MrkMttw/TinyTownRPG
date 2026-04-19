import pygame
import math
from core.config import WIN_WIDTH, WIN_HEIGHT, SETTINGS

pygame.init()

# Initialize mixer for audio
pygame.mixer.init()

# Load background music from settings
bgm_path = SETTINGS.get("BGM_PATH", "assets/esefex/bg_sfx.mp3")
try:
    pygame.mixer.music.load(bgm_path)
    # Play background music if enabled
    if SETTINGS["BGM_ENABLED"]:
        pygame.mixer.music.set_volume(SETTINGS["BGM_VOLUME"])
        pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Error loading initial background music: {e}")

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

# Load assets with error handling
try:
    bg = pygame.image.load("assets/Background4.png").convert()
    bg_width = bg.get_width()
    bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))
except pygame.error as e:
    print(f"Error loading background: {e}")
    bg = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill((100, 100, 100))
    bg_width = WIN_WIDTH

try:
    LOGO = pygame.image.load("assets/Logo.png")
except pygame.error as e:
    print(f"Error loading logo: {e}")
    LOGO = None

try:
    OUTLINE = pygame.image.load("assets/Outline.png")
    OUTLINE = pygame.transform.scale(OUTLINE, (400, 300))
except pygame.error as e:
    print(f"Error loading outline: {e}")
    OUTLINE = None

try:
    BOY = pygame.image.load("assets/boyslct.png")
except pygame.error as e:
    print(f"Error loading boy sprite: {e}")
    BOY = None

try:
    GIRL = pygame.image.load("assets/girlslct.png")
except pygame.error as e:
    print(f"Error loading girl sprite: {e}")
    GIRL = None

try:
    BUTTON1 = pygame.image.load("assets/Button1.png")
except pygame.error as e:
    print(f"Error loading button1: {e}")
    BUTTON1 = None

try:
    BUTTON2 = pygame.image.load("assets/Button2.png")
except pygame.error as e:
    print(f"Error loading button2: {e}")
    BUTTON2 = None

try:
    BOY_PANEL = pygame.image.load("assets/cutscenes/boy_panel.png")
except pygame.error as e:
    print(f"Error loading boy panel: {e}")
    BOY_PANEL = None

try:
    GIRL_PANEL = pygame.image.load("assets/cutscenes/girl_panel.png")
except pygame.error as e:
    print(f"Error loading girl panel: {e}")
    GIRL_PANEL = None

# Scrolling variables
tiles = math.ceil(WIN_WIDTH / bg_width) + 1


def get_font(size):
    # Get font from assets
    return pygame.font.Font("assets/font.ttf", size)


def draw_scrolling_bg(scroll, speed=1.2):
    """
    Draw scrolling background and return updated scroll value
    
    Args:
        scroll: Current scroll position
        speed: Scroll speed (default: 1.2)
        
    Returns:
        Updated scroll position
    """
    for i in range(tiles):
        SCREEN.blit(bg, (i * bg_width + scroll, 0))
    
    scroll -= speed
    if abs(scroll) > bg_width:
        scroll = 0
    
    return scroll


"""
Shared variables and functions for the game
"""