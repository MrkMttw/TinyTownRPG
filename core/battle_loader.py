import pygame
from core.shared import WIN_WIDTH, WIN_HEIGHT, get_font
from core.gamedata import gamedata


def load_battle_assets(npc=None):
    """
    Load assets for the battle screen

    Args:
        npc: NPC object for opponent data (optional)

    Returns:
        tuple: (bg, left_char, right_char, player_pet, enemy_pet)
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

    # Load player character
    left_char = pygame.image.load(left_path).convert_alpha()
    print(f"[DEBUG] Left char loaded, original size: {left_char.get_size()}")
    left_char = pygame.transform.scale_by(left_char, 0.3)  # zoom in for battle portrait
    print(f"[DEBUG] Left char scaled, new size: {left_char.get_size()}")

    # Load enemy character (use NPC sprite if provided, otherwise default)
    if npc and hasattr(npc, 'sprite_path'):
        enemy_path = npc.sprite_path
    else:
        enemy_path = "assets/characters/Boy/boy_left_stand.png"

    right_char = pygame.image.load(enemy_path).convert_alpha()
    print(f"[DEBUG] Right char loaded, original size: {right_char.get_size()}")
    right_char = pygame.transform.scale_by(right_char, 0.3)
    print(f"[DEBUG] Right char scaled, new size: {right_char.get_size()}")

    # Load player pet
    player_pet_val = gamedata["in_game_data"][0]["PET"]
    player_pet_name = get_pet_name(player_pet_val)
    player_pet = load_pet_stance(player_pet_name, "def")  # Default to defense stance
    if player_pet:
        # Scale pet to 25% of original size (smaller for battle)
        player_pet = pygame.transform.scale_by(player_pet, 0.25)
        print(f"[DEBUG] Player pet loaded: {player_pet_name}, size: {player_pet.get_size()}")

    # Load enemy pet (if NPC has one)
    enemy_pet = None
    if npc and hasattr(npc, 'pet') and npc.pet:
        enemy_pet_name = npc.pet
        enemy_pet = load_pet_stance(enemy_pet_name, "def")  # Default to defense stance
        if enemy_pet:
            # Scale pet to 25% of original size (smaller for battle)
            enemy_pet = pygame.transform.scale_by(enemy_pet, 0.25)
            print(f"[DEBUG] Enemy pet loaded: {enemy_pet_name}, size: {enemy_pet.get_size()}")

    print(f"[DEBUG] Returning assets")
    return bg, left_char, right_char, player_pet, enemy_pet


def get_pet_name(pet_val):
    """
    Convert pet value to pet name

    Args:
        pet_val: Pet value from gamedata

    Returns:
        str: Pet name
    """
    pet_names = {
        1: "sausage",
        2: "balls",
        3: "bear",
        4: "dino",
        5: "germs",
        6: "pom"
    }
    return pet_names.get(pet_val, "sausage")


def load_pet_stance(pet_name, stance):
    """
    Load pet stance image

    Args:
        pet_name: Name of the pet (e.g., "sausage", "balls")
        stance: Stance to load ("attack", "def", "break")

    Returns:
        pygame.Surface: Pet stance image or None if not found
    """
    # Map stance names to file suffixes
    stance_map = {
        "attack": "attack",
        "defense": "def",
        "def": "def",
        "break": "break"
    }
    suffix = stance_map.get(stance, "def")
    
    try:
        path = f"assets/battle_actions/{pet_name}_{suffix}.png"
        pet_img = pygame.image.load(path).convert_alpha()
        return pet_img
    except FileNotFoundError:
        print(f"[WARNING] Pet stance not found: {path}")
        return None


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
