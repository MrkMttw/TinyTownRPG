import pygame
import sys
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font, BUTTON1
from components.battle_actions import draw_enemy_actions, draw_player_actions
from components.pause_menu import PauseMenu
from core.battle_loader import load_battle_assets, draw_health_bar, load_pet_stance, get_pet_name
from core.battle_mechanics import process_queued_turn, generate_enemy_actions
from core.gamedata import gamedata

def battlefield_screen(action_queue=None, player_hp=None, enemy_hp=None, npc=None):
    """
    Battle screen with queue-based turns.
    If action_queue is provided, executes all 3 turns automatically.
    Accepts initial HP values from previous rounds.
    
    Args:
        action_queue: List of player actions
        player_hp: Current player HP
        enemy_hp: Current enemy HP
        npc: NPC object for opponent data
    """
    bg, left_char, right_char, player_pet, enemy_pet = load_battle_assets(npc)
    
    # Initialize pause menu
    pause_menu = PauseMenu()

    # Load player attributes from gamedata
    player_data = gamedata["player_data"][0]
    player_level = player_data.get("LEVEL", 1)
    # Base stats: HP=100, Attack=20, multiplied by level
    player_max_hp = 100 * player_level
    player_attack = 20 * player_level

    # Initialize HP if not provided (first round)
    if player_hp is None:
        # Get player HP from gamedata or use max
        player_hp = player_data.get("HP", player_max_hp)
    if enemy_hp is None:
        # Initialize enemy HP to max (with level multiplier)
        enemy_hp = enemy_max_hp

    # Enemy attributes from NPC or default
    if npc:
        enemy_level = npc.level
        enemy_name = npc.name
    else:
        enemy_level = 1
        enemy_name = "Enemy"
    # Base stats: HP=100, Attack=19, multiplied by level
    enemy_max_hp = 100 * enemy_level
    enemy_attack = 19 * enemy_level

    battle_msg = "A fierce battle begins!"
    msg_timer = 2000
    state = "message"  # "message", "executing", "game_over"

    # Queue-based battle system
    current_turn_index = 0
    max_turns = 3 if action_queue else 0
    
    # Generate enemy actions for all turns at once
    enemy_actions = generate_enemy_actions(max_turns) if action_queue else []

    left_rect = left_char.get_rect(midbottom=(WIN_WIDTH * 0.25, WIN_HEIGHT - 150))
    right_rect = right_char.get_rect(midbottom=(WIN_WIDTH * 0.75, WIN_HEIGHT - 150))
    
    # Pet positions (beside their owners)
    player_pet_rect = None
    enemy_pet_rect = None
    if player_pet:
        player_pet_rect = player_pet.get_rect(midleft=(left_rect.right + 10, left_rect.centery))
    if enemy_pet:
        enemy_pet_rect = enemy_pet.get_rect(midright=(right_rect.left - 10, right_rect.centery))
    
    # Pet stance tracking
    current_player_pet_stance = "def"
    current_enemy_pet_stance = "def"
    player_pet_name = get_pet_name(gamedata["in_game_data"][0]["PET"])
    enemy_pet_name = npc.pet if npc and npc.pet else None
    
    clock = pygame.time.Clock()

    while True:
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        # Get delta time
        dt = clock.tick(60)

        # Handle pause menu if active
        if pause_menu.active:
            pause_result = pause_menu.handle_events()
            if pause_result == "quit":
                # Exit battle and return to game engine
                pygame.event.clear()
                return player_hp, enemy_hp, True
            pause_menu.draw(SCREEN)
            pygame.display.update()
            continue  # Skip game logic when paused

        for event in pygame.event.get():
            # Handle quit event
            if event.type == pygame.QUIT:
                # Quit the game
                pygame.quit()
                sys.exit()
            
            # Handle pause toggle
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu.toggle()

        # Draw game elements
        # Render background and combatants
        SCREEN.blit(bg, (0, 0))
        SCREEN.blit(left_char, left_rect)
        SCREEN.blit(right_char, right_rect)
        
        # Draw pets beside their owners
        if player_pet and player_pet_rect:
            SCREEN.blit(player_pet, player_pet_rect)
        if enemy_pet and enemy_pet_rect:
            SCREEN.blit(enemy_pet, enemy_pet_rect)
        
        # Show opponent name and level above enemy head
        enemy_info_text = get_font(24).render(f"{enemy_name} Lv.{enemy_level}", True, (255, 255, 255))
        enemy_info_rect = enemy_info_text.get_rect(midtop=(right_rect.centerx, right_rect.top - 35))
        pygame.draw.rect(SCREEN, (0, 0, 0), enemy_info_rect.inflate(10, 5))
        SCREEN.blit(enemy_info_text, enemy_info_rect)

        # Render UI
        draw_health_bar(SCREEN, 50, 50, 400, 30, player_hp, player_max_hp, "PLAYER")
        draw_health_bar(
            SCREEN, WIN_WIDTH - 450, 50, 400, 30, enemy_hp, enemy_max_hp, "ENEMY"
        )
        
        # Draw player actions at bottom left
        draw_player_actions(SCREEN, action_queue, current_turn_index)
        
        # Draw enemy actions at bottom right
        draw_enemy_actions(SCREEN, enemy_actions, current_turn_index)

        # Show turn indicator
        if action_queue and current_turn_index < max_turns:
            # Render turn indicator text
            turn_text = get_font(25).render(f"Turn {current_turn_index + 1} of {max_turns}", True, (255, 255, 200))
            turn_rect = turn_text.get_rect(center=(WIN_WIDTH // 2, 180))
            SCREEN.blit(turn_text, turn_rect)

        if battle_msg:
            # Render battle message
            msg_surf = get_font(28).render(battle_msg, True, "Black")
            msg_rect = msg_surf.get_rect(center=(WIN_WIDTH // 2, 120))
            bg_rect = msg_rect.inflate(40, 20)
            pygame.draw.rect(SCREEN, (255, 255, 255), bg_rect)
            pygame.draw.rect(SCREEN, (0, 0, 0), bg_rect, 3)
            SCREEN.blit(msg_surf, msg_rect)

        # Game state logic (only runs when not paused)
        if state == "message":
            # Decrease message timer
            msg_timer -= dt
            if msg_timer <= 0:
                if player_hp <= 0 or enemy_hp <= 0:
                    state = "game_over"
                    battle_msg = "VICTORY!" if enemy_hp <= 0 else "DEFEAT!"
                    msg_timer = 3000
                else:
                    # Execute next queued turn
                    if action_queue and current_turn_index < max_turns:
                        # Get pre-generated enemy action for this turn
                        current_enemy_action = enemy_actions[current_turn_index] if current_turn_index < len(enemy_actions) else None
                        player_action = action_queue[current_turn_index] if current_turn_index < len(action_queue) else "defense"
                        
                        # Normalize player action
                        if player_action == "defend":
                            player_action = "defense"
                        
                        # Update pet stances based on actions
                        current_player_pet_stance = player_action if player_action in ["attack", "defense", "break"] else "def"
                        current_enemy_pet_stance = current_enemy_action if current_enemy_action in ["attack", "defense", "break"] else "def"
                        
                        # Reload pet sprites with new stances
                        if player_pet_name:
                            new_player_pet = load_pet_stance(player_pet_name, current_player_pet_stance)
                            if new_player_pet:
                                player_pet = pygame.transform.scale_by(new_player_pet, 0.5)
                        
                        if enemy_pet_name:
                            new_enemy_pet = load_pet_stance(enemy_pet_name, current_enemy_pet_stance)
                            if new_enemy_pet:
                                enemy_pet = pygame.transform.scale_by(new_enemy_pet, 0.5)
                        
                        player_hp, enemy_hp, battle_msg = process_queued_turn(
                            action_queue, current_turn_index,
                            player_hp, enemy_hp,
                            player_attack, enemy_attack,
                            current_enemy_action
                        )
                        current_turn_index += 1
                        state = "message"
                        msg_timer = 2500  # Longer delay to read both actions
                    else:
                        # All turns complete or no queue
                        state = "game_over"
                        if enemy_hp <= 0:
                            battle_msg = "VICTORY!"
                        elif player_hp <= 0:
                            battle_msg = "DEFEAT!"
                        else:
                            battle_msg = "Round Complete!"
                        msg_timer = 3000

        elif state == "game_over":
            # Decrease message timer
            msg_timer -= dt
            if msg_timer <= 0:
                # Show victory/defeat panel
                char_id = gamedata["in_game_data"][0]["CHARACTER"]
                if enemy_hp <= 0:
                    # Victory
                    if char_id == 1:
                        panel_path = "assets/banner/girl_vic.png"
                    else:
                        panel_path = "assets/banner/boy_vic.png"
                    # Implement level-up and pet collection
                    if npc and player_level == npc.level:
                        # Level up
                        gamedata["player_data"][0]["LEVEL"] += 1
                        # Add pet to collection if not already owned
                        if npc.pet and npc.pet not in gamedata.get("pets_collected", []):
                            if "pets_collected" not in gamedata:
                                gamedata["pets_collected"] = []
                            gamedata["pets_collected"].append(npc.pet)
                            from core.gamedata import update_game_data
                            update_game_data()
                    victory = True
                else:
                    # Defeat
                    if char_id == 1:
                        panel_path = "assets/banner/girl_defeat.png"
                    else:
                        panel_path = "assets/banner/boy_defeat.png"
                    victory = False
                
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
                                    waiting = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                                    waiting = False
                except FileNotFoundError:
                    print(f"[WARNING] Panel not found: {panel_path}")
                
                # Return HP status: (player_hp, enemy_hp, battle_ended)
                battle_ended = player_hp <= 0 or enemy_hp <= 0
                return player_hp, enemy_hp, battle_ended

        pygame.display.update()
