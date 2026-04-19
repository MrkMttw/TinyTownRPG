import pygame, sys, json
from core.shared import *
from components.button import Button
from components.textbox import TextBox
from core.config import *
from screens.character_selection import character_selection_screen
from core.gamedata import gamedata, update_game_data


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
        """
        Handle character selection and proceed to name entry
        
        Args:
            char_id: Character ID (0 for boy, 1 for girl)
            
        Returns:
            None
        """
        # Set character in game data
        gamedata["in_game_data"][0]["CHARACTER"] = char_id
        # Update game data
        update_game_data()
        # Proceed to name entry
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
    """
    Name entry screen
    
    Args:
        on_character_selected: callback function for when a character is selected
        back: callback function for when the back button is clicked
        gamedata: game data
        update_game_data: function to update game data
        
    Returns:
        None
    """
    # Initialize scroll position
    scroll = 0

    # Create name text box
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
        """
        Main game loop for name entry
        
        Returns:
            None
        """
        # Get mouse position
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        # scrolling background
        scroll = draw_scrolling_bg(scroll, 1.2)

        # Render title text
        ENTER_NAME_TEXT = get_font(80).render("ENTER YOUR NAME", True, "Black")
        ENTER_NAME_RECT = ENTER_NAME_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(ENTER_NAME_TEXT, ENTER_NAME_RECT)

        # Create back button
        OPTIONS_BACK = Button(
            #Back button
            image=BUTTON2,
            pos=(150, 70),
            text_input="BACK",
            font=get_font(30),
            base_color="BLACK",
            hovering_color="#FFE14D",
        )

        # Create next button
        OPTIONS_NEXT = Button(
            #Next button
            image=BUTTON2,
            pos=(660, 500),
            text_input="NEXT",
            font=get_font(30),
            base_color="BLACK",
            hovering_color="#FFE14D",
        )

        # Update buttons
        for button in [OPTIONS_BACK, OPTIONS_NEXT]:
            # Change button color based on mouse position
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        # Update name text box
        name_textbox.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit game
                pygame.quit()
                sys.exit()

            result = name_textbox.handle_event(event)
            if result is not None:
                # Enter pressed, call callback with the name
                gamedata["player_data"][0]["NAME"] = result
                update_game_data()
                intro_comic_panel()
                return  # proceed to game

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if Next button was clicked
                if OPTIONS_NEXT.checkForInput(OPTIONS_MOUSE_POS):
                    # Get name from text box
                    gamedata["player_data"][0]["NAME"] = name_textbox.get_text()
                    update_game_data()
                    intro_comic_panel()
                    return  # proceed to game
                    
                # Check if Back button was clicked
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    # Go back to character selection
                    return character_selection(
                        on_character_selected,
                        back,
                        gamedata,
                        update_game_data,
                    )  # go back

        pygame.display.update()


def intro_comic_panel():
    """
    Intro comic panel screen that displays based on character selection
    
    Shows boy_panel if character is 2, girl_panel if character is 1
    """
    scroll = 0
    
    # Get character ID from gamedata
    char_id = gamedata["in_game_data"][0]["CHARACTER"]
    
    # Select appropriate panel based on character
    if char_id == 2:
        panel_image = BOY_PANEL
    else:
        panel_image = GIRL_PANEL
    
    # Scale panel to fit screen
    panel_scaled = pygame.transform.scale(panel_image, (WIN_WIDTH, WIN_HEIGHT))
    
    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        
        # Draw the comic panel
        SCREEN.blit(panel_scaled, (0, 0))
        
        # Create borderless next button at bottom right
        NEXT_BUTTON = Button(
            image=None,
            pos=(WIN_WIDTH - 100, WIN_HEIGHT - 50),
            text_input="NEXT",
            font=get_font(30),
            base_color="WHITE",
            hovering_color="#FFE14D",
        )
        
        NEXT_BUTTON.changeColor(MOUSE_POS)
        NEXT_BUTTON.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NEXT_BUTTON.checkForInput(MOUSE_POS):
                    return
        
        pygame.display.update()


def tutorial_controls():
    """
    Tutorial screen that teaches player controls (WASD, TAB, ESC)
    
    After completing this tutorial, IF_PLAYED will be set to 1
    """
    scroll = 0
    
    # Tutorial state: 0 = WASD, 1 = TAB, 2 = ESC, 3 = Complete
    tutorial_step = 0
    
    while True:
        TUTORIAL_MOUSE_POS = pygame.mouse.get_pos()
        
        # Scrolling background
        scroll = draw_scrolling_bg(scroll, 1)
        
        # Title
        TITLE_TEXT = get_font(60).render("TUTORIAL", True, "Black")
        TITLE_RECT = TITLE_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(TITLE_TEXT, TITLE_RECT)
        
        # Tutorial content based on current step
        if tutorial_step == 0:
            # WASD controls
            INSTRUCTION_TEXT = get_font(35).render("Use WASD to move your character", True, "Black")
            INSTRUCTION_RECT = INSTRUCTION_TEXT.get_rect(center=(640, 250))
            SCREEN.blit(INSTRUCTION_TEXT, INSTRUCTION_RECT)
            
            KEYS_TEXT = get_font(50).render("W = Up  A = Left  S = Down  D = Right", True, (50, 50, 200))
            KEYS_RECT = KEYS_TEXT.get_rect(center=(640, 320))
            SCREEN.blit(KEYS_TEXT, KEYS_RECT)
            
            HINT_TEXT = get_font(25).render("Press any WASD key to continue...", True, (100, 100, 100))
            HINT_RECT = HINT_TEXT.get_rect(center=(640, 450))
            SCREEN.blit(HINT_TEXT, HINT_RECT)
            
        elif tutorial_step == 1:
            # TAB controls
            INSTRUCTION_TEXT = get_font(35).render("Press TAB to open pet inventory", True, "Black")
            INSTRUCTION_RECT = INSTRUCTION_TEXT.get_rect(center=(640, 250))
            SCREEN.blit(INSTRUCTION_TEXT, INSTRUCTION_RECT)
            
            KEYS_TEXT = get_font(50).render("TAB", True, (50, 50, 200))
            KEYS_RECT = KEYS_TEXT.get_rect(center=(640, 320))
            SCREEN.blit(KEYS_TEXT, KEYS_RECT)
            
            HINT_TEXT = get_font(25).render("Press TAB to continue...", True, (100, 100, 100))
            HINT_RECT = HINT_TEXT.get_rect(center=(640, 450))
            SCREEN.blit(HINT_TEXT, HINT_RECT)
            
        elif tutorial_step == 2:
            # ESC controls
            INSTRUCTION_TEXT = get_font(35).render("Press ESC to pause the game", True, "Black")
            INSTRUCTION_RECT = INSTRUCTION_TEXT.get_rect(center=(640, 250))
            SCREEN.blit(INSTRUCTION_TEXT, INSTRUCTION_RECT)
            
            KEYS_TEXT = get_font(50).render("ESC", True, (50, 50, 200))
            KEYS_RECT = KEYS_TEXT.get_rect(center=(640, 320))
            SCREEN.blit(KEYS_TEXT, KEYS_RECT)
            
            HINT_TEXT = get_font(25).render("Press ESC to continue...", True, (100, 100, 100))
            HINT_RECT = HINT_TEXT.get_rect(center=(640, 450))
            SCREEN.blit(HINT_TEXT, HINT_RECT)
            
        elif tutorial_step == 3:
            # Tutorial complete
            INSTRUCTION_TEXT = get_font(40).render("Tutorial Complete!", True, (0, 150, 0))
            INSTRUCTION_RECT = INSTRUCTION_TEXT.get_rect(center=(640, 250))
            SCREEN.blit(INSTRUCTION_TEXT, INSTRUCTION_RECT)
            
            SUMMARY_TEXT = get_font(30).render("You now know the basic controls.", True, "Black")
            SUMMARY_RECT = SUMMARY_TEXT.get_rect(center=(640, 320))
            SCREEN.blit(SUMMARY_TEXT, SUMMARY_RECT)
            
            # Continue button
            CONTINUE_BUTTON = Button(
                image=BUTTON1,
                pos=(640, 450),
                text_input="CONTINUE",
                font=get_font(35),
                base_color="BLACK",
                hovering_color="#FFE14D",
            )
            CONTINUE_BUTTON.changeColor(TUTORIAL_MOUSE_POS)
            CONTINUE_BUTTON.update(SCREEN)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if tutorial_step == 0:
                    # Check for WASD keys
                    if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                        tutorial_step = 1
                elif tutorial_step == 1:
                    # Check for TAB
                    if event.key == pygame.K_TAB:
                        tutorial_step = 2
                elif tutorial_step == 2:
                    # Check for ESC
                    if event.key == pygame.K_ESCAPE:
                        tutorial_step = 3
            
            if event.type == pygame.MOUSEBUTTONDOWN and tutorial_step == 3:
                if CONTINUE_BUTTON.checkForInput(TUTORIAL_MOUSE_POS):
                    # Set IF_PLAYED to 1 after tutorial completion
                    gamedata["in_game_data"][0]["IF_PLAYED"] = 1
                    update_game_data()
                    return
        
        pygame.display.update()
