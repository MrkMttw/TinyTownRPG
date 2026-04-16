import pygame, sys, json
from core.shared import *
from components.button import Button
from components.textbox import TextBox
from core.config import *
from screens.character_selection import character_selection_screen


def character_selection(
    on_character_selected,
    back,
    gamedata,
    update_game_data,
):
    """
    Character selection screen

    Attributes:
        on_character_selected: callback function for when a character is selected
        back: callback function for when the back button is clicked
        gamedata: game data
        update_game_data: function to update game data
        proceed_to_name: callback function for when a character is selected
        scroll: scroll position
        OPTIONS_MOUSE_POS: mouse position
        BOY_RECT: rectangle of the boy image
        GIRL_RECT: rectangle of the girl image
        OUTLINE_RECT: rectangle of the outline image
        OPTIONS_TEXT1: text of the options screen
        OPTIONS_TEXT2: text of the options screen
        OPTIONS_TEXT3: text of the options screen
        OPTIONS_BOY_SELECTED: button for selecting the boy
        OPTIONS_GIRL_SELECTED: button for selecting the girl
        OPTIONS_BACK: button for going back

    Parameters:
        None
    """

    # This function handles what happens AFTER a character is clicked in the tutorial
    def proceed_to_name(char_id):
        gamedata["in_game_data"][0]["CHARACTER"] = char_id
        update_game_data()
        return enter_name(
            on_character_selected,
            back,
            gamedata,
            update_game_data,
        )

    # Call the shared screen logic
    return character_selection_screen(
        proceed_to_name,
        back,
    )


def enter_name(
    on_character_selected,
    back,
    gamedata,
    update_game_data,
):
    scroll = 0

    name_textbox = TextBox(
        image=None,
        pos=(640, 360),
        text_input="",
        font=get_font(40),
        base_color="BLACK",
        hovering_color="YELLOW",
        box_color=(255, 255, 255),
        border_color="BLACK",
        border_width=2,
        width=400,
        height=60,
    )
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        # scrolling background
        for i in range(tiles):
            SCREEN.blit(bg, (i * bg_width + scroll, 0))

        scroll -= 1.2
        if abs(scroll) > bg_width:
            scroll = 0

        ENTER_NAME_TEXT = get_font(80).render("ENTER YOUR NAME", True, "Black")
        ENTER_NAME_RECT = ENTER_NAME_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(ENTER_NAME_TEXT, ENTER_NAME_RECT)

        OPTIONS_BACK = Button(
            image=BUTTON2,
            pos=(150, 70),
            text_input="BACK",
            font=get_font(30),
            base_color="BLACK",
            hovering_color="#FFE14D",
        )

        OPTIONS_NEXT = Button(
            image=BUTTON2,
            pos=(660, 500),
            text_input="NEXT",
            font=get_font(30),
            base_color="BLACK",
            hovering_color="#FFE14D",
        )

        for button in [OPTIONS_BACK, OPTIONS_NEXT]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        name_textbox.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            result = name_textbox.handle_event(event)
            if result is not None:
                # Enter pressed, call callback with the name
                gamedata["player_data"][0]["NAME"] = result
                update_game_data()
                return  # proceed to game

            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_NEXT.checkForInput(OPTIONS_MOUSE_POS):
                    gamedata["player_data"][0]["NAME"] = name_textbox.get_text()
                    update_game_data()
                    return  # proceed to game
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return character_selection(
                        on_character_selected,
                        back,
                        gamedata,
                        update_game_data,
                    )  # go back

        pygame.display.update()
