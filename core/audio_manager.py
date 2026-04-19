import pygame
from core.config import SETTINGS


def play_battle_music():
    """Stop background music and play battle music."""
    pygame.mixer.music.pause()
    battle_music_path = SETTINGS.get("BATTLE_MUSIC_PATH", "assets/esefex/battle_sfx.mp3")
    try:
        pygame.mixer.music.load(battle_music_path)
        if SETTINGS["BGM_ENABLED"]:
            pygame.mixer.music.set_volume(SETTINGS["BGM_VOLUME"])
            pygame.mixer.music.play(-1)  # Loop battle music
    except pygame.error as e:
        print(f"Error loading battle music: {e}")


def resume_bgm():
    """Stop current music and resume background music."""
    pygame.mixer.music.stop()
    bgm_path = SETTINGS.get("BGM_PATH", "assets/esefex/bg_sfx.mp3")
    try:
        pygame.mixer.music.load(bgm_path)
        if SETTINGS["BGM_ENABLED"]:
            pygame.mixer.music.set_volume(SETTINGS["BGM_VOLUME"])
            pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Error loading background music: {e}")


def load_battle_sfx():
    """Load battle sound effects from settings.
    
    Returns:
        dict: Dictionary of sound effects with keys: attack, defense, breakarmor, victory, defeat
    """
    sfx_paths = SETTINGS.get("SFX_PATHS", {})
    return {
        "attack": pygame.mixer.Sound(sfx_paths.get("attack", "assets/esefex/attack_sfx.mp3")),
        "defense": pygame.mixer.Sound(sfx_paths.get("defense", "assets/esefex/defense_sfx.mp3")),
        "breakarmor": pygame.mixer.Sound(sfx_paths.get("breakarmor", "assets/esefex/breakarmor_sfx.mp3")),
        "victory": pygame.mixer.Sound(sfx_paths.get("victory", "assets/esefex/victory_sfx.mp3")),
        "defeat": pygame.mixer.Sound(sfx_paths.get("defeat", "assets/esefex/defeat_sfx.mp3"))
    }
