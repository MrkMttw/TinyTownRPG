import pygame
import sys
import random
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font, BUTTON1
from components.button import Button
from core.gamedata import gamedata


def load_battle_assets():
    """
    Load assets for the battle screen

    Returns:
    """
    print("[DEBUG] Loading battle assets...")

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
    pygame.draw.rect(
        surface, (0, 0, 0), (x - 2, y - 2, width + 4, height + 4)
    )
    pygame.draw.rect(surface, (255, 0, 0), (x, y, width, height))
    ratio = max(0, current_hp) / max_hp
    pygame.draw.rect(surface, (0, 255, 0), (x, y, width * ratio, height))

    name_text = get_font(30).render(name, True, (255, 255, 255))
    surface.blit(name_text, (x, y - 40))


def process_attack(attacker, defender, is_break, defender_is_defending):
    dmg_base = random.randint(10, 20)

    if is_break:
        if defender_is_defending:
            dmg = int(dmg_base * 1.5)
            msg = f"{attacker} BROKE defense! {dmg} DMG!"
        else:
            dmg = int(dmg_base * 0.5)
            msg = f"{attacker} tried to break... missed! {dmg} DMG."
    else:
        if defender_is_defending:
            dmg = int(dmg_base * 0.3)
            msg = f"{defender} blocked! {dmg} DMG."
        else:
            dmg = dmg_base
            msg = f"{attacker} attacks! {dmg} DMG!"

    return dmg, msg


def process_queued_turn(action_queue, turn_index, player_hp, enemy_hp, player_defending, enemy_defending):
    """
    Process a single turn from the action queue.
    Returns: (new_player_hp, new_enemy_hp, new_player_defending, new_enemy_defending, battle_msg)
    """
    if turn_index >= len(action_queue):
        return player_hp, enemy_hp, player_defending, enemy_defending, "Round complete!"

    player_action = action_queue[turn_index]

    # Process Player Action
    if player_action == "defend":
        player_defending = True
        battle_msg = "Player defends!"
    elif player_action == "attack":
        dmg, msg = process_attack("Player", "Enemy", False, enemy_defending)
        enemy_hp -= dmg
        battle_msg = msg
    elif player_action == "break":
        dmg, msg = process_attack("Player", "Enemy", True, enemy_defending)
        enemy_hp -= dmg
        battle_msg = msg

    # Check if enemy is defeated before enemy turn
    if enemy_hp <= 0:
        return player_hp, enemy_hp, player_defending, enemy_defending, battle_msg

    # Process Enemy Turn (after player action)
    action_choice = random.choice(["attack", "attack", "defend", "break"])
    if action_choice == "defend":
        enemy_defending = True
        battle_msg += " | Enemy defends!"
    else:
        dmg, msg = process_attack("Enemy", "Player", action_choice == "break", player_defending)
        player_hp -= dmg
        battle_msg += f" | {msg}"

    return player_hp, enemy_hp, player_defending, enemy_defending, battle_msg


def battlefield_screen(action_queue=None, player_hp=100, enemy_hp=100):
    """
    Battle screen with queue-based turns.
    If action_queue is provided, executes all 3 turns automatically.
    Accepts initial HP values from previous rounds.
    """
    bg, left_char, right_char = load_battle_assets()

    player_max_hp = 100
    enemy_max_hp = 100

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
        mouse_pos = pygame.mouse.get_pos()
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
            turn_text = get_font(25).render(f"Turn {current_turn_index + 1} of {max_turns}", True, (255, 255, 200))
            turn_rect = turn_text.get_rect(center=(WIN_WIDTH // 2, 180))
            SCREEN.blit(turn_text, turn_rect)

        if battle_msg:
            msg_surf = get_font(28).render(battle_msg, True, "Black")
            msg_rect = msg_surf.get_rect(center=(WIN_WIDTH // 2, 120))
            bg_rect = msg_rect.inflate(40, 20)
            pygame.draw.rect(SCREEN, (255, 255, 255), bg_rect)
            pygame.draw.rect(SCREEN, (0, 0, 0), bg_rect, 3)
            SCREEN.blit(msg_surf, msg_rect)

        if state == "message":
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
                            player_hp, enemy_hp, player_defending, enemy_defending
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
            msg_timer -= dt
            if msg_timer <= 0:
                # Return HP status: (player_hp, enemy_hp, battle_ended)
                battle_ended = player_hp <= 0 or enemy_hp <= 0
                return player_hp, enemy_hp, battle_ended

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
