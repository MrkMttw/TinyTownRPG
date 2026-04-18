import pygame
import sys
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font, BUTTON1
from components.button import Button
from core.battle_loader import load_battle_assets, draw_health_bar
from core.battle_mechanics import process_attack, process_queued_turn
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
    # Calculate attack and defense based on level
    player_attack = 15 + (player_level * 2)
    player_defense = 15 + player_level

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
    # Calculate enemy attack and defense based on level
    enemy_attack = 10 + (enemy_level * 2)
    enemy_defense = 10 + enemy_level

    player_defending = False
    enemy_defending = False

    battle_msg = "A fierce battle begins!"
    msg_timer = 2000
    state = "message"  # "message", "executing", "game_over"

    # Queue-based battle system
    current_turn_index = 0
    max_turns = 3 if action_queue else 0

    left_rect = left_char.get_rect(midbottom=(WIN_WIDTH * 0.25, WIN_HEIGHT - 150))
    right_rect = right_char.get_rect(midbottom=(WIN_WIDTH * 0.75, WIN_HEIGHT - 150))

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
                        player_hp, enemy_hp, player_defending, enemy_defending, battle_msg = process_queued_turn(
                            action_queue, current_turn_index,
                            player_hp, enemy_hp, player_defending, enemy_defending,
                            player_attack, player_defense, enemy_attack, enemy_defense
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
