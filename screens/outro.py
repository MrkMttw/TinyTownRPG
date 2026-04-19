import pygame
import sys
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font
from core.config import SETTINGS
from core.gamedata import gamedata, update_game_data, reset_game_data


def outro_screen():
    """
    Outro screen shown when player reaches level 7.
    Displays victory message and offers option to reset progress.
    
    Returns:
        bool: True if reset was chosen (should exit to homescreen), False otherwise
    """
    # Stop any playing music
    pygame.mixer.music.stop()
    
    # Load victory music if available
    try:
        victory_music_path = SETTINGS.get("VICTORY_MUSIC_PATH", "assets/esefex/victory_sfx.mp3")
        pygame.mixer.music.load(victory_music_path)
        if SETTINGS["BGM_ENABLED"]:
            pygame.mixer.music.set_volume(SETTINGS["BGM_VOLUME"])
            pygame.mixer.music.play(-1)
    except:
        pass
    
    clock = pygame.time.Clock()
    
    # Load background
    try:
        bg = pygame.image.load("assets/Background4.png").convert()
        bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))
    except FileNotFoundError:
        bg = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        bg.fill((50, 50, 100))
    
    # Button setup
    font = get_font(30)
    title_font = get_font(50)
    
    # Create buttons
    yes_button_rect = pygame.Rect(0, 0, 200, 60)
    yes_button_rect.center = (WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2 + 100)
    
    no_button_rect = pygame.Rect(0, 0, 200, 60)
    no_button_rect.center = (WIN_WIDTH // 2 + 150, WIN_HEIGHT // 2 + 100)
    
    running = True
    reset_chosen = False
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if yes_button_rect.collidepoint(event.pos):
                        reset_chosen = True
                        running = False
                    elif no_button_rect.collidepoint(event.pos):
                        reset_chosen = False
                        running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reset_chosen = False
                    running = False
        
        # Draw background
        SCREEN.blit(bg, (0, 0))
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        SCREEN.blit(overlay, (0, 0))
        
        # Draw title
        title_text = title_font.render("The Mad Scientist has been defeated!", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50))
        SCREEN.blit(title_text, title_rect)
        
        # Draw subtitle
        subtitle_text = font.render("Thank you Adventurer!", True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 20))
        SCREEN.blit(subtitle_text, subtitle_rect)
        
        # Draw question
        question_text = font.render("Would you like to reset your progress?", True, (200, 200, 200))
        question_rect = question_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 60))
        SCREEN.blit(question_text, question_rect)
        
        # Draw YES button
        yes_color = (100, 200, 100) if yes_button_rect.collidepoint(mouse_pos) else (80, 180, 80)
        pygame.draw.rect(SCREEN, yes_color, yes_button_rect, border_radius=10)
        pygame.draw.rect(SCREEN, (255, 255, 255), yes_button_rect, 3, border_radius=10)
        yes_text = font.render("YES", True, (255, 255, 255))
        yes_text_rect = yes_text.get_rect(center=yes_button_rect.center)
        SCREEN.blit(yes_text, yes_text_rect)
        
        # Draw NO button
        no_color = (200, 100, 100) if no_button_rect.collidepoint(mouse_pos) else (180, 80, 80)
        pygame.draw.rect(SCREEN, no_color, no_button_rect, border_radius=10)
        pygame.draw.rect(SCREEN, (255, 255, 255), no_button_rect, 3, border_radius=10)
        no_text = font.render("NO", True, (255, 255, 255))
        no_text_rect = no_text.get_rect(center=no_button_rect.center)
        SCREEN.blit(no_text, no_text_rect)
        
        pygame.display.update()
    
    # Stop music
    pygame.mixer.music.stop()
    
    # Reset progress if chosen
    if reset_chosen:
        reset_game_data()
    
    # Clear events
    pygame.event.clear()
    
    return reset_chosen
