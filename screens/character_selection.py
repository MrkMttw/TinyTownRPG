import pygame, sys, math
from core.shared import *
from components.button import Button


def character_selection_screen(on_select_callback, back_callback):
    """
    Character selection screen

    Attributes:
        on_select_callback: callback function for when a character is selected
        back_callback: callback function for when the back button is clicked
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
    scroll = 0
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        # Scrolling background logic
        for i in range(tiles):
            SCREEN.blit(bg, (i * bg_width + scroll, 0))

        scroll -= 1.2
        if abs(scroll) > bg_width:
            scroll = 0

        # UI Elements
        BOY_RECT = BOY.get_rect(center=(250, 360))
        GIRL_RECT = GIRL.get_rect(center=(600, 360))
        OUTLINE_RECT = OUTLINE.get_rect(center=(1000, 360))

        OPTIONS_TEXT1 = get_font(80).render("SELECT", True, "Black")
        OPTIONS_TEXT2 = get_font(80).render("YOUR", True, "Black")
        OPTIONS_TEXT3 = get_font(80).render("CHARACTER", True, "Black")

        SCREEN.blit(BOY, BOY_RECT)
        SCREEN.blit(GIRL, GIRL_RECT)
        SCREEN.blit(OUTLINE, OUTLINE_RECT)
        SCREEN.blit(OPTIONS_TEXT1, OPTIONS_TEXT1.get_rect(center=(1000, 260)))
        SCREEN.blit(OPTIONS_TEXT2, OPTIONS_TEXT2.get_rect(center=(1000, 360)))
        SCREEN.blit(OPTIONS_TEXT3, OPTIONS_TEXT3.get_rect(center=(1000, 460)))

        # Buttons
        OPTIONS_BOY_SELECTED = Button(
            image=BUTTON1,
            pos=(240, 600),
            text_input="SELECT",
            font=get_font(40),
            base_color="BLACK",
            hovering_color="#FFE14D",
        )

        OPTIONS_GIRL_SELECTED = Button(
            image=BUTTON1,
            pos=(590, 600),
            text_input="SELECT",
            font=get_font(40),
            base_color="BLACK",
            hovering_color="#FFE14D",
        )

        OPTIONS_BACK = Button(
            image=BUTTON2,
            pos=(150, 70),
            text_input="BACK",
            font=get_font(30),
            base_color="BLACK",
            hovering_color="#FFE14D",
        )

        for button in [OPTIONS_BOY_SELECTED, OPTIONS_BACK, OPTIONS_GIRL_SELECTED]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BOY_SELECTED.checkForInput(OPTIONS_MOUSE_POS):
                    # Set character to Boy (2) and trigger callback
                    return on_select_callback(2)
                if OPTIONS_GIRL_SELECTED.checkForInput(OPTIONS_MOUSE_POS):
                    # Set character to Girl (1) and trigger callback
                    return on_select_callback(1)
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return back_callback()

        pygame.display.update()


# ================= CHARACTER IS SELECTED =================
def character_selected():
    """
    Character selected screen

    Attributes:
        scroll: scroll position
        OPTIONS_MOUSE_POS: mouse position
        CHARACTER_SELECTED: text of the character selected screen
        CHARACTER_SELECTED_RECT: rectangle of the character selected text
        SELECTED_BACK: button for going back

    Parameters:
        None
    """
    scroll = 0
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        # scrolling background
        for i in range(tiles):
            SCREEN.blit(bg, (i * bg_width + scroll, 0))

        scroll -= 0.4
        if abs(scroll) > bg_width:
            scroll = 0

        CHARACTER_SELECTED = get_font(80).render(
            "CHARACTER HAS BEEN SELECTED", True, "Black"
        )
        CHARACTER_SELECTED_RECT = CHARACTER_SELECTED.get_rect(center=(640, 260))
        SCREEN.blit(CHARACTER_SELECTED, CHARACTER_SELECTED_RECT)

        SELECTED_BACK = Button(
            image=BUTTON2,
            pos=(640, 500),
            text_input="BACK",
            font=get_font(30),
            base_color="Black",
            hovering_color="#FFE14D",
        )

        SELECTED_BACK.changeColor(OPTIONS_MOUSE_POS)
        SELECTED_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if SELECTED_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return

        pygame.display.update()
