import pygame, sys, json
from button import Button
from textbox import TextBox
from config import *
from character_selection import character_selection_screen # Import the new file

def character_selection(SCREEN, tiles, bg, bg_width, BOY, GIRL, OUTLINE, BUTTON1, BUTTON2, ButtonClass, get_font, on_character_selected, back, gamedata, update_game_data):
    
    # This function handles what happens AFTER a character is clicked in the tutorial
    def proceed_to_name(char_id):
        gamedata["in_game_data"][0]["CHARACTER"] = char_id
        update_game_data()
        return enter_name(SCREEN, tiles, bg, bg_width, BOY, GIRL, OUTLINE, BUTTON1, BUTTON2, ButtonClass, get_font, on_character_selected, back, gamedata, update_game_data)

    # Call the shared screen logic
    return character_selection_screen(
        SCREEN, tiles, bg, bg_width, BOY, GIRL, OUTLINE, BUTTON1, BUTTON2, 
        ButtonClass, get_font, proceed_to_name, back
    )

def enter_name(SCREEN, tiles, bg, bg_width, BOY, GIRL, OUTLINE, BUTTON1, BUTTON2, ButtonClass, get_font, on_character_selected, back,gamedata, update_game_data):
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
        height=60
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

        OPTIONS_BACK = Button(image=BUTTON2, pos=(150, 70), 
                                text_input="BACK", font=get_font(30), 
                                base_color="BLACK", hovering_color="#FFE14D")
        
        OPTIONS_NEXT = Button(image=BUTTON2, pos=(660, 500), 
                              text_input="NEXT", font=get_font(30), 
                              base_color="BLACK", hovering_color="#FFE14D")

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
                return # proceed to game


            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_NEXT.checkForInput(OPTIONS_MOUSE_POS):
                    gamedata["player_data"][0]["NAME"] = name_textbox.get_text()
                    update_game_data()
                    return # proceed to game
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return character_selection(SCREEN, tiles, bg, bg_width, BOY, GIRL, OUTLINE, BUTTON1, BUTTON2, ButtonClass, get_font, on_character_selected, back, gamedata, update_game_data)# go back

        pygame.display.update()