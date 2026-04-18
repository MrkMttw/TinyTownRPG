import pygame
import sys
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font, BUTTON1
from components.button import Button
from core.battle_loader import load_battle_assets, draw_health_bar
from core.battle_mechanics import process_queued_turn, generate_enemy_actions
from core.gamedata import gamedata

def battlefield_screen(action_queue=None, player_hp=None, enemy_hp=None):
    """
    Battle screen with queue-based turns.
    If action_queue is provided, executes all 3 turns automatically.
    Accepts initial HP values from previous rounds.
    """
    bg, left_char, right_char = load_battle_assets()

    # Load player attributes from gamedata
    player_data = gamedata["player_data"][0]
    player_max_hp = player_data.get("MAX_HP", 100)
    player_level = player_data.get("LEVEL", 1)
    # Calculate attack based on level
    player_attack = 15 + (player_level * 2)

    # Initialize HP if not provided (first round)
    if player_hp is None:
        # Get player HP from gamedata
        player_hp = player_data.get("HP", player_max_hp)
    if enemy_hp is None:
        # Initialize enemy HP to max
        enemy_hp = 100

    # Enemy attributes from opponent_data
    opponent_data = gamedata.get("opponent_data", [{"LEVEL": 1}])[0]
    enemy_max_hp = opponent_data.get("MAX_HP", 100)
    enemy_level = opponent_data.get("LEVEL", 1)
    # Calculate enemy attack based on level
    enemy_attack = 10 + (enemy_level * 2)

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
    
    def draw_enemy_actions(surface, enemy_actions, current_turn_index):
        """
        Draw enemy actions at the bottom right of the screen.
        
        Args:
            surface: Pygame surface to draw on
            enemy_actions: List of enemy actions
            current_turn_index: Current turn index (to highlight current action)
        """
        if not enemy_actions:
            return
        
        # Position for enemy actions display (bottom right)
        start_x = WIN_WIDTH - 350
        start_y = WIN_HEIGHT - 180
        box_width = 300
        box_height = 150
        
        # Draw background box
        pygame.draw.rect(surface, (50, 50, 50), (start_x, start_y, box_width, box_height))
        pygame.draw.rect(surface, (255, 255, 255), (start_x, start_y, box_width, box_height), 3)
        
        # Draw title
        title_text = get_font(24).render("Enemy Actions", True, (255, 200, 100))
        title_rect = title_text.get_rect(center=(start_x + box_width // 2, start_y + 25))
        surface.blit(title_text, title_rect)
        
        # Draw each action
        for i, action in enumerate(enemy_actions):
            # Determine color based on action type
            if action == "attack":
                color = (255, 100, 100)  # Red for attack
            elif action == "defense":
                color = (100, 100, 255)  # Blue for defense
            elif action == "break":
                color = (255, 165, 0)    # Orange for break armor
            else:
                color = (200, 200, 200)  # Gray for unknown
            
            # Highlight current action
            if i == current_turn_index:
                pygame.draw.rect(surface, (255, 255, 0), (start_x + 20, start_y + 50 + i * 30, box_width - 40, 25), 2)
            
            # Draw action text
            action_text = get_font(20).render(f"{i + 1}. {action.upper()}", True, color)
            surface.blit(action_text, (start_x + 30, start_y + 52 + i * 30))
    
    def draw_player_actions(surface, player_actions, current_turn_index):
        """
        Draw player actions at the bottom left of the screen.
        
        Args:
            surface: Pygame surface to draw on
            player_actions: List of player actions
            current_turn_index: Current turn index (to highlight current action)
        """
        if not player_actions:
            return
        
        # Position for player actions display (bottom left)
        start_x = 50
        start_y = WIN_HEIGHT - 180
        box_width = 300
        box_height = 150
        
        # Draw background box
        pygame.draw.rect(surface, (50, 50, 50), (start_x, start_y, box_width, box_height))
        pygame.draw.rect(surface, (255, 255, 255), (start_x, start_y, box_width, box_height), 3)
        
        # Draw title
        title_text = get_font(24).render("Your Actions", True, (100, 255, 100))
        title_rect = title_text.get_rect(center=(start_x + box_width // 2, start_y + 25))
        surface.blit(title_text, title_rect)
        
        # Draw each action
        for i, action in enumerate(player_actions):
            # Normalize action name
            if action == "defend":
                action = "defense"
            
            # Determine color based on action type
            if action == "attack":
                color = (255, 100, 100)  # Red for attack
            elif action == "defense":
                color = (100, 100, 255)  # Blue for defense
            elif action == "break":
                color = (255, 165, 0)    # Orange for break armor
            else:
                color = (200, 200, 200)  # Gray for unknown
            
            # Highlight current action
            if i == current_turn_index:
                pygame.draw.rect(surface, (255, 255, 0), (start_x + 20, start_y + 50 + i * 30, box_width - 40, 25), 2)
            
            # Draw action text
            action_text = get_font(20).render(f"{i + 1}. {action.upper()}", True, color)
            surface.blit(action_text, (start_x + 30, start_y + 52 + i * 30))

    clock = pygame.time.Clock()

    while True:
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        # Get delta time
        dt = clock.tick(60)

        # Render background and combatants
        SCREEN.blit(bg, (0, 0))
        SCREEN.blit(left_char, left_rect)
        SCREEN.blit(right_char, right_rect)

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
                # Return HP status: (player_hp, enemy_hp, battle_ended)
                battle_ended = player_hp <= 0 or enemy_hp <= 0
                return player_hp, enemy_hp, battle_ended

        for event in pygame.event.get():
            # Handle quit event
            if event.type == pygame.QUIT:
                # Quit the game
                pygame.quit()
                sys.exit()

        pygame.display.update()
