import pygame
import sys
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font
from core.gamedata import gamedata
from core.audio_manager import resume_bgm


def show_battle_result_panel(is_victory, npc=None, player_level=None):
    """
    Display victory or defeat panel with continue button.
    Handles level-up and pet collection logic for victories.
    
    Args:
        is_victory: Boolean indicating if player won
        npc: NPC object for opponent data (for level-up logic)
        player_level: Current player level
        
    Returns:
        bool: True if game should exit to homescreen (level 7 victory), False otherwise
    """
    # Stop battle music before playing victory/defeat sounds
    pygame.mixer.music.stop()
    
    # Load sound effects
    sfx_paths = gamedata.get("SETTINGS", {}).get("SFX_PATHS", {})
    if is_victory:
        pygame.mixer.Sound(sfx_paths.get("victory", "assets/esefex/victory_sfx.mp3")).play()
    else:
        pygame.mixer.Sound(sfx_paths.get("defeat", "assets/esefex/defeat_sfx.mp3")).play()
    
    # Determine panel path based on character and result
    char_id = gamedata["in_game_data"][0]["CHARACTER"]
    if is_victory:
        panel_path = "assets/banner/girl_vic.png" if char_id == 1 else "assets/banner/boy_vic.png"
    else:
        panel_path = "assets/banner/girl_defeat.png" if char_id == 1 else "assets/banner/boy_defeat.png"
    
    # Handle victory logic (level-up and pet collection)
    exit_to_homescreen = False
    if is_victory and npc and player_level == npc.level:
        # Level up
        gamedata["player_data"][0]["LEVEL"] += 1
        
        # Add pet to collection if not already owned
        if npc.pet and npc.pet not in gamedata.get("pets_collected", []):
            if "pets_collected" not in gamedata:
                gamedata["pets_collected"] = []
            gamedata["pets_collected"].append(npc.pet)
            from core.gamedata import update_game_data
            update_game_data()
        
        # Check if player reached level 7 - trigger outro
        if gamedata["player_data"][0]["LEVEL"] == 7:
            from screens.outro import outro_screen
            should_exit = outro_screen()
            if should_exit:
                resume_bgm()
                pygame.event.clear()
                return True  # Exit to homescreen
    
    # Load and display panel
    try:
        panel = pygame.image.load(panel_path).convert_alpha()
        panel = pygame.transform.scale(panel, (WIN_WIDTH // 2, WIN_HEIGHT // 2))
        panel_rect = panel.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2))
        
        # Draw panel with semi-transparent overlay
        overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        SCREEN.blit(overlay, (0, 0))
        SCREEN.blit(panel, panel_rect)
        
        # Add continue button
        button_rect = pygame.Rect(0, 0, 200, 50)
        button_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2 + panel_rect.height // 2 + 50)
        pygame.draw.rect(SCREEN, (100, 100, 100), button_rect)
        button_text = get_font(24).render("Continue", True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        SCREEN.blit(button_text, button_text_rect)
        
        pygame.display.update()
        
        # Wait for continue button click
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        resume_bgm()
                        waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        resume_bgm()
                        waiting = False
    except FileNotFoundError:
        print(f"[WARNING] Panel not found: {panel_path}")
    
    return False  # Don't exit to homescreen by default
