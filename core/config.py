import json
import os

WIN_WIDTH = 1280
WIN_HEIGHT = 720
TILESIZE = 64
FPS = 60

PET_SIZE = 32
PET_SPEED = 1
PLAYER_LAYER = 1
PLAYER_SPEED = 1
SPRINT_MULTIPLIER = 2.0

# Pet data: maps pet value to (path, name) tuple
PET_PATHS = {
    1: ("assets/pets/Sausage", "sausage"),
    2: ("assets/pets/Bear", "bear"),
    3: ("assets/pets/Germs", "germs"),
    4: ("assets/pets/Pompoms", "pom"),
    5: ("assets/pets/Dino", "dino"),
    6: ("assets/pets/Balls", "balls"),
}

# Tile visibility: 1 = visible, 2 = invisible
TILES_VISIBLE = 1

# Default settings
DEFAULT_SETTINGS = {
    "SFX_ENABLED": True,
    "SFX_VOLUME": 0.5,
    "BGM_ENABLED": True,
    "BGM_VOLUME": 0.5,
    "FULLSCREEN": False,
    "BGM_PATH": "assets/esefex/bg_sfx.mp3",
    "BATTLE_MUSIC_PATH": "assets/esefex/battle_sfx.mp3",
    "SFX_PATHS": {
        "attack": "assets/esefex/attack_sfx.mp3",
        "defense": "assets/esefex/defense_sfx.mp3",
        "breakarmor": "assets/esefex/breakarmor_sfx.mp3",
        "victory": "assets/esefex/victory_sfx.mp3",
        "defeat": "assets/esefex/defeat_sfx.mp3",
        "boss": "assets/esefex/boss_sfx.mp3",
        "boy": "assets/esefex/boy_sfx.mp3",
        "girl": "assets/esefex/girl_sfx.mp3"
    }
}

# Load settings from JSON file, or use defaults
settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "core", "settings.json")
try:
    with open(settings_path, "r", encoding="utf-8") as f:
        loaded_settings = json.load(f)
        # Merge loaded settings with defaults (in case new settings are added later)
        settings = {**DEFAULT_SETTINGS, **loaded_settings}
except FileNotFoundError:
    settings = DEFAULT_SETTINGS.copy()

# Settings dictionary - use this for dynamic access
SETTINGS = settings

# Backwards compatibility - access through SETTINGS dict
SFX_ENABLED = SETTINGS["SFX_ENABLED"]
SFX_VOLUME = SETTINGS["SFX_VOLUME"]
BGM_ENABLED = SETTINGS["BGM_ENABLED"]
BGM_VOLUME = SETTINGS["BGM_VOLUME"]
FULLSCREEN = SETTINGS["FULLSCREEN"]


def save_settings(sfx_enabled, sfx_volume, bgm_enabled, bgm_volume, fullscreen):
    """Save settings to JSON file

    Args:
        sfx_enabled: Boolean for sound effects toggle
        sfx_volume: Float for sound effects volume (0.0-1.0)
        bgm_enabled: Boolean for background music toggle
        bgm_volume: Float for background music volume (0.0-1.0)
        fullscreen: Boolean for fullscreen mode
    """
    global SFX_ENABLED, SFX_VOLUME, BGM_ENABLED, BGM_VOLUME, FULLSCREEN, SETTINGS
    
    settings_to_save = {
        "SFX_ENABLED": sfx_enabled,
        "SFX_VOLUME": sfx_volume,
        "BGM_ENABLED": bgm_enabled,
        "BGM_VOLUME": bgm_volume,
        "FULLSCREEN": fullscreen,
        "BGM_PATH": SETTINGS.get("BGM_PATH", DEFAULT_SETTINGS["BGM_PATH"]),
        "BATTLE_MUSIC_PATH": SETTINGS.get("BATTLE_MUSIC_PATH", DEFAULT_SETTINGS["BATTLE_MUSIC_PATH"]),
        "SFX_PATHS": SETTINGS.get("SFX_PATHS", DEFAULT_SETTINGS["SFX_PATHS"])
    }
    settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "core", "settings.json")
    with open(settings_path, "w", encoding="utf-8") as f:
        json.dump(settings_to_save, f, indent=4)
    
    # Update SETTINGS dictionary
    SETTINGS["SFX_ENABLED"] = sfx_enabled
    SETTINGS["SFX_VOLUME"] = sfx_volume
    SETTINGS["BGM_ENABLED"] = bgm_enabled
    SETTINGS["BGM_VOLUME"] = bgm_volume
    SETTINGS["FULLSCREEN"] = fullscreen
    
    # Update module-level variables to stay in sync
    SFX_ENABLED = sfx_enabled
    SFX_VOLUME = sfx_volume
    BGM_ENABLED = bgm_enabled
    BGM_VOLUME = bgm_volume
    FULLSCREEN = fullscreen