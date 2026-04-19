from core.game_engine import *
from core.gamedata import *
from screens.character_selection import *
from screens.tutorial import *
from screens.settings import show_settings
from components.button import *
from components.textbox import *
from core.config import *
from core.shared import *


# ================= PLAY =================
def play():
    """
    Play screen

    Attributes:
        None

    Parameters:
        None
    """
    if gamedata["in_game_data"][0]["IF_PLAYED"] == 0:  # first time playing
        update_game_data()
        character_selection(
            None,
            lambda: None,  # no backward navigation for first boot
            gamedata,
            update_game_data,
        )
        # Show tutorial controls (IF_PLAYED will be set to 1 after tutorial completion)
        tutorial_controls()

    game = Game(SCREEN)
    game.new()

    while game.playing:
        # Handle events
        game.events()
        # Update game state
        game.update()
        # Draw everything
        game.draw()

    # Clear events to prevent input bugs
    pygame.event.clear()
    return


# ================= OPTIONS =================
def settings():
    """
    Options screen

    Parameters:
        None
    """
    show_settings()
