import pygame
import sys
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font, BUTTON1
from components.battle_actions import draw_enemy_actions, draw_player_actions
from components.pause_menu import PauseMenu
from components.battle_result_panel import show_battle_result_panel
from core.battle_loader import load_battle_assets, draw_health_bar, load_pet_stance, get_pet_name, update_pet_sprite
from core.battle_mechanics import process_queued_turn, generate_enemy_actions
from core.gamedata import gamedata
from core.config import SETTINGS
from core.audio_manager import play_battle_music, resume_bgm, load_battle_sfx

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
        
    Returns:
        tuple: (player_hp, enemy_hp, battle_ended, exit_to_homescreen)
               exit_to_homescreen is True when player resets after level 7 victory
    """
    bg, left_char, right_char, player_pet, enemy_pet = load_battle_assets(npc)
    if enemy_pet:
        enemy_pet = pygame.transform.flip(enemy_pet, True, False)
    
    # Play battle music
    play_battle_music()
    
    # Load sound effects
    sfx = load_battle_sfx()
    
    # Initialize pause menu
    pause_menu = PauseMenu()

    # Load player attributes from gamedata
    player_data = gamedata["player_data"][0]
    player_level = player_data.get("LEVEL", 1)
    # Base stats: HP=100, Attack=20, multiplied by level
    player_max_hp = 100 * player_level
    player_attack = 20 * player_level

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

    # Initialize HP if not provided (first round)
    if player_hp is None:
        # Set player HP to max for new battle
        player_hp = player_max_hp
    if enemy_hp is None:
        # Initialize enemy HP to max (with level multiplier)
        enemy_hp = enemy_max_hp

    battle_msg = "A fierce battle begins!"
    msg_timer = 2000
    state = "message"  # "message", "stand_before", "action", "stand_after", "game_over"
    stand_timer = 1000  # Duration for stand animations (1 second)
    action_timer = 1500  # Duration for action animations (1.5 seconds)

    # Queue-based battle system
    current_turn_index = 0
    max_turns = 3 if action_queue else 0
    
    # Generate enemy actions for all turns at once
    enemy_actions = generate_enemy_actions(max_turns) if action_queue else []

    # Pet positions (fixed screen positions)
    player_pet_rect = None
    enemy_pet_rect = None
    if player_pet:
        player_pet_rect = player_pet.get_rect(midbottom=(WIN_WIDTH * 0.25, WIN_HEIGHT - 150))
    if enemy_pet:
        enemy_pet_rect = enemy_pet.get_rect(midbottom=(WIN_WIDTH * 0.75, WIN_HEIGHT - 150))
    
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
                # Resume background music before exiting
                resume_bgm()
                # Exit battle and return to game engine
                pygame.event.clear()
                return player_hp, enemy_hp, True, False
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
        # Render background
        SCREEN.blit(bg, (0, 0))
        
        # Draw pets beside their owners
        if player_pet and player_pet_rect:
            SCREEN.blit(player_pet, player_pet_rect)
        if enemy_pet and enemy_pet_rect:
            SCREEN.blit(enemy_pet, enemy_pet_rect)
        

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
                    # Start next queued turn with stand animation
                    if action_queue and current_turn_index < max_turns:
                        state = "stand_before"
                        stand_timer = 1000  # Show stand for 1 second before action
                        # Set both pets to stand stance
                        current_player_pet_stance = "stand"
                        current_enemy_pet_stance = "stand"
                        
                        # Reload pet sprites with stand stance
                        if player_pet_name:
                            player_pet = update_pet_sprite(player_pet_name, current_player_pet_stance)
                        
                        if enemy_pet_name:
                            enemy_pet = update_pet_sprite(enemy_pet_name, current_enemy_pet_stance, flip_horizontal=True)
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

        elif state == "stand_before":
            # Show stand animation before the action
            stand_timer -= dt
            if stand_timer <= 0:
                # Move to action state
                state = "action"
                action_timer = 1500  # Show action for 1.5 seconds
                
                # Get actions for this turn
                current_enemy_action = enemy_actions[current_turn_index] if current_turn_index < len(enemy_actions) else None
                player_action = action_queue[current_turn_index] if current_turn_index < len(action_queue) else "defense"
                
                # Normalize player action
                if player_action == "defend":
                    player_action = "defense"
                
                # Update pet stances based on actions
                current_player_pet_stance = player_action if player_action in ["attack", "defense", "break"] else "def"
                current_enemy_pet_stance = current_enemy_action if current_enemy_action in ["attack", "defense", "break"] else "def"
                
                # Play action SFX
                if player_action == "attack":
                    sfx["attack"].play()
                elif player_action == "defense":
                    sfx["defense"].play()
                elif player_action == "break":
                    sfx["breakarmor"].play()
                
                # Reload pet sprites with action stances
                if player_pet_name:
                    player_pet = update_pet_sprite(player_pet_name, current_player_pet_stance)
                
                if enemy_pet_name:
                    enemy_pet = update_pet_sprite(enemy_pet_name, current_enemy_pet_stance, flip_horizontal=True)

        elif state == "action":
            # Show action animation
            action_timer -= dt
            if action_timer <= 0:
                # Process the turn logic
                current_enemy_action = enemy_actions[current_turn_index] if current_turn_index < len(enemy_actions) else None
                player_action = action_queue[current_turn_index] if current_turn_index < len(action_queue) else "defense"
                
                if player_action == "defend":
                    player_action = "defense"
                
                player_hp, enemy_hp, battle_msg = process_queued_turn(
                    action_queue, current_turn_index,
                    player_hp, enemy_hp,
                    player_attack, enemy_attack,
                    current_enemy_action
                )
                
                # Move to stand_after state
                state = "stand_after"
                stand_timer = 1000  # Show stand for 1 second after action
                
                # Set both pets to stand stance
                current_player_pet_stance = "stand"
                current_enemy_pet_stance = "stand"
                
                # Reload pet sprites with stand stance
                if player_pet_name:
                    player_pet = update_pet_sprite(player_pet_name, current_player_pet_stance)
                
                if enemy_pet_name:
                    enemy_pet = update_pet_sprite(enemy_pet_name, current_enemy_pet_stance, flip_horizontal=True)
                
                current_turn_index += 1

        elif state == "stand_after":
            # Show stand animation after the action
            stand_timer -= dt
            if stand_timer <= 0:
                # Move to message state to show battle result
                state = "message"
                msg_timer = 2000

        elif state == "game_over":
            # Decrease message timer
            msg_timer -= dt
            if msg_timer <= 0:
                # Only show panel if battle actually ended (someone's HP <= 0)
                if player_hp > 0 and enemy_hp > 0:
                    # Round complete with both alive - return without panel
                    resume_bgm()
                    return player_hp, enemy_hp, False, False
                
                # Show victory/defeat panel
                is_victory = enemy_hp <= 0
                exit_to_homescreen = show_battle_result_panel(is_victory, npc, player_level)
                
                # Return HP status: (player_hp, enemy_hp, battle_ended, exit_to_homescreen)
                battle_ended = player_hp <= 0 or enemy_hp <= 0
                
                return player_hp, enemy_hp, battle_ended, exit_to_homescreen

        pygame.display.update()
