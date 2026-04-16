import json

gamedata = {
    "in_game_data": [
        {
            "IF_PLAYED": 0,
            "CHARACTER": 1,
            "PET": 1
        }
    ],
    "player_data": [
        {
            "NAME": "",
            "LEVEL": 1,
            "XP": 0,
            "HP": 100,
            "MONEY": 0
        }
    ]
}

try:
    with open("gamedata.json", "r", encoding="utf-8") as f:
        gamedata = json.load(f)
except FileNotFoundError:
    pass

def update_game_data():
    with open("gamedata.json", "w", encoding="utf-8") as f:
        json.dump(gamedata, f, indent=4)