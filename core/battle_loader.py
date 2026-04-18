import pygame
from core.shared import WIN_WIDTH, WIN_HEIGHT, get_font
from core.gamedata import gamedata


def load_battle_assets():
    """
    Load assets for the battle screen

    Returns:
    """
    print("[DEBUG] Loading battle assets...")

    # Load background
    bg = pygame.image.load("assets/maps/DomainExpansion.png").convert()
    bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))
    print(f"[DEBUG] Background loaded, size: {bg.get_size()}")

    char_id = gamedata["in_game_data"][0]["CHARACTER"]
    print(f"[DEBUG] Character ID: {char_id}")

    if char_id == 1:  # Girl
        left_path = "assets/characters/Girl/girl_right_stand.png"
    else:  # Boy
        left_path = "assets/characters/Boy/boy_right_stand.png"

    enemy_path = "assets/characters/Boy/boy_left_stand.png"

    print(f"[DEBUG] Left path (player): {left_path}")
    print(f"[DEBUG] Right path (enemy): {enemy_path}")

    left_char = pygame.image.load(left_path).convert_alpha()
    print(f"[DEBUG] Left char loaded, original size: {left_char.get_size()}")
    left_char = pygame.transform.scale_by(left_char, 0.3)  # zoom in for battle portrait
    print(f"[DEBUG] Left char scaled, new size: {left_char.get_size()}")

    right_char = pygame.image.load(enemy_path).convert_alpha()
    print(f"[DEBUG] Right char loaded, original size: {right_char.get_size()}")
    right_char = pygame.transform.scale_by(right_char, 0.3)
    print(f"[DEBUG] Right char scaled, new size: {right_char.get_size()}")

    print(f"[DEBUG] Returning assets - left_char size: {left_char.get_size()}, right_char size: {right_char.get_size()}")
    return bg, left_char, right_char


def draw_health_bar(surface, x, y, width, height, current_hp, max_hp, name):
    """
    Draw a health bar on the screen
    
    Args:
        surface: Pygame surface to draw on
        x: X position of the health bar
        y: Y position of the health bar
        width: Width of the health bar
        height: Height of the health bar
        current_hp: Current health points
        max_hp: Maximum health points
        name: Name of the entity
        
    Returns:
        None
    """
    # Draw border
    pygame.draw.rect(
        surface, (0, 0, 0), (x - 2, y - 2, width + 4, height + 4)
    )
    # Draw red background
    pygame.draw.rect(surface, (255, 0, 0), (x, y, width, height))
    # Draw green foreground
    ratio = max(0, current_hp) / max_hp
    pygame.draw.rect(surface, (0, 255, 0), (x, y, width * ratio, height))

    # Draw name
    name_text = get_font(30).render(name, True, (255, 255, 255))
    surface.blit(name_text, (x, y - 40))
