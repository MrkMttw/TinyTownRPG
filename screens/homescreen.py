from core.game_engine import *
from core.gamedata import *
from screens.character_selection import *
from screens.tutorial import *
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
        gamedata["in_game_data"][0]["IF_PLAYED"] = 1
        update_game_data()

    # gamedata["in_game_data"][0]["IF_PLAYED"] = 1

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
def options():
    """
    Options screen

    Attributes:
        save_and_confirm: callback function for when a character is selected
        go_back: callback function for when the back button is clicked

    Parameters:
        None
    """

    # Callback for when a character is selected in Options
    def save_and_confirm(char_id):
        # Save selected character
        gamedata["in_game_data"][0]["CHARACTER"] = char_id
        update_game_data()
        # Show confirmation screen
        return character_selected()

    # Callback for the back button
    def go_back():
        # Simply exits the function to return to main_menu loop
        return

    # Use the separated character selection screen
    character_selection_screen(
        save_and_confirm,
        go_back,
    )
