import json

# Initialize game data with default values
gamedata = {
    "in_game_data": [{"IF_PLAYED": 0, "CHARACTER": 1, "PET": 1}],
    "player_data": [{"NAME": "", "LEVEL": 1, "XP": 0, "HP": 100}],
    "pets_collected": ["sausage",],
}

try:
    # Try to load existing game data
    with open("core/gamedata.json", "r", encoding="utf-8") as f:
        gamedata = json.load(f)
except FileNotFoundError:
    # If file doesn't exist, use default data
    pass


def update_game_data():
    # Update game data to JSON file
    with open("core/gamedata.json", "w", encoding="utf-8") as f:
        json.dump(gamedata, f, indent=4)


def reset_game_data():
    """
    Reset game data to default values.
    
    This function resets all game progress including:
    - IF_PLAYED flag
    - Character selection
    - Pet selection
    - Player level and stats
    - Collected pets
    """
    global gamedata
    gamedata = {
        "in_game_data": [{"IF_PLAYED": 0, "CHARACTER": 1, "PET": 1}],
        "player_data": [{"NAME": "", "LEVEL": 1, "XP": 0, "HP": 100}],
        "pets_collected": ["sausage",],
    }
    update_game_data()
