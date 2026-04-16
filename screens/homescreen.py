from core.game_engine import *
from core.gamedata import *
from screens.character_selection import *
from screens.tutorial import *
from components.button import *
from components.textbox import *
from core.config import *


# ================= PLAY =================
def play(SCREEN, tiles, bg, bg_width, BOY, GIRL, OUTLINE, BUTTON1, BUTTON2, Button, get_font, main_menu):
    if gamedata["in_game_data"][0]["IF_PLAYED"] == 0:  # first time playing
        update_game_data()
        character_selection(
            SCREEN,
            tiles,
            bg,
            bg_width,
            BOY,
            GIRL,
            OUTLINE,
            BUTTON1,
            BUTTON2,
            Button,
            get_font,
            character_selected,
            main_menu,
            gamedata,
            update_game_data,
        )

    # gamedata["in_game_data"][0]["IF_PLAYED"] = 1

    game = Game(SCREEN)
    game.new()

    while game.playing:
        game.events()
        game.update()
        game.draw()

    pygame.event.clear()  # prevent input bugs
    return


# ================= OPTIONS =================
def options(SCREEN, tiles, bg, bg_width, BOY, GIRL, OUTLINE, BUTTON1, BUTTON2, Button, get_font, main_menu):
    # Callback for when a character is selected in Options
    def save_and_confirm(char_id):
        gamedata["in_game_data"][0]["CHARACTER"] = char_id
        update_game_data()
        return character_selected(
            SCREEN, tiles, bg, bg_width, get_font, BUTTON2, Button, main_menu
        )  # Show confirmation screen

    # Callback for the back button
    def go_back():
        return  # Simply exits the function to return to main_menu loop

    # Use the separated character selection screen
    character_selection_screen(
        SCREEN,
        tiles,
        bg,
        bg_width,
        BOY,
        GIRL,
        OUTLINE,
        BUTTON1,
        BUTTON2,
        Button,
        get_font,
        save_and_confirm,
        go_back,
    )
