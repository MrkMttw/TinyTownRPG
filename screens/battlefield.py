import pygame
import sys
import random
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font, BUTTON1
from components.button import Button


def load_battle_assets():
    """
    Load assets for the battle screen

    Returns:
    """
    bg = pygame.image.load("assets/maps/DomainExpansion.png").convert()
    bg = pygame.transform.scale(bg, (WIN_WIDTH, WIN_HEIGHT))

    # Left character: girl_left_stand
    left_char = pygame.image.load(
        "assets/characters/Girl/girl_left_stand.png"
    ).convert_alpha()
    left_char = pygame.transform.flip(left_char, True, False)  # flip to face right
    left_char = pygame.transform.scale_by(left_char, 6)  # zoom in for battle portrait

    # Right character: boy_right_stand
    right_char = pygame.image.load(
        "assets/characters/Boy/boy_right_stand.png"
    ).convert_alpha()
    right_char = pygame.transform.flip(right_char, True, False)  # flip to face left
    right_char = pygame.transform.scale_by(right_char, 6)

    return bg, left_char, right_char


def draw_health_bar(surface, x, y, width, height, current_hp, max_hp, name):
    pygame.draw.rect(
        surface, (0, 0, 0), (x - 2, y - 2, width + 4, height + 4)
    )  # Outline
    pygame.draw.rect(surface, (255, 0, 0), (x, y, width, height))  # Back
    ratio = max(0, current_hp) / max_hp
    pygame.draw.rect(surface, (0, 255, 0), (x, y, width * ratio, height))  # Front

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


def battlefield_screen():
    bg, left_char, right_char = load_battle_assets()

    player_max_hp = 100
    player_hp = 100
    enemy_max_hp = 100
    enemy_hp = 100

    player_defending = False
    enemy_defending = False

    turn = "player"
    battle_msg = "A fierce battle begins!"
    msg_timer = 2000
    state = "message"  # "menu", "message", "game_over"

    left_rect = left_char.get_rect(midbottom=(WIN_WIDTH * 0.25, WIN_HEIGHT - 150))
    right_rect = right_char.get_rect(midbottom=(WIN_WIDTH * 0.75, WIN_HEIGHT - 150))

    btn_y = WIN_HEIGHT - 70
    ATTACK_BTN = Button(
        image=BUTTON1,
        pos=(WIN_WIDTH * 0.25, btn_y),
        text_input="ATTACK",
        font=get_font(35),
        base_color="BLACK",
        hovering_color="#FFE14D",
    )
    DEFEND_BTN = Button(
        image=BUTTON1,
        pos=(WIN_WIDTH * 0.5, btn_y),
        text_input="DEFEND",
        font=get_font(35),
        base_color="BLACK",
        hovering_color="#FFE14D",
    )
    BREAK_BTN = Button(
        image=BUTTON1,
        pos=(WIN_WIDTH * 0.75, btn_y),
        text_input="BREAK ARMOR",
        font=get_font(35),
        base_color="BLACK",
        hovering_color="#FFE14D",
    )

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

        if battle_msg:
            msg_surf = get_font(30).render(battle_msg, True, "Black")
            msg_rect = msg_surf.get_rect(
                center=(WIN_WIDTH // 2, 125)
            )  # change the location of battle message
            bg_rect = msg_rect.inflate(40, 20)
            pygame.draw.rect(SCREEN, (255, 255, 255), bg_rect)
            pygame.draw.rect(SCREEN, (0, 0, 0), bg_rect, 3)
            SCREEN.blit(msg_surf, msg_rect)

        if state == "menu" and turn == "player":
            for btn in [ATTACK_BTN, DEFEND_BTN, BREAK_BTN]:
                btn.changeColor(mouse_pos)
                btn.update(SCREEN)

        elif state == "message":
            msg_timer -= dt
            if msg_timer <= 0:
                if player_hp <= 0 or enemy_hp <= 0:
                    state = "game_over"
                    battle_msg = "VICTORY!" if enemy_hp <= 0 else "DEFEAT!"
                    msg_timer = 3000
                else:
                    if turn == "player":
                        turn = "enemy"
                        player_defending = False

                        # Process Enemy Turn
                        action_choice = random.choice(
                            ["attack", "attack", "defend", "break"]
                        )
                        if action_choice == "defend":
                            enemy_defending = True
                            battle_msg = "Enemy assumes a defensive stance!"
                        else:
                            dmg, battle_msg = process_attack(
                                "Enemy",
                                "Player",
                                action_choice == "break",
                                player_defending,
                            )
                            player_hp -= dmg

                        state = "message"
                        msg_timer = 2000
                    else:
                        turn = "player"
                        enemy_defending = False
                        state = "menu"
                        battle_msg = ""

        elif state == "game_over":
            msg_timer -= dt
            if msg_timer <= 0:
                return  # Battle is finished

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and state == "menu"
                and turn == "player"
            ):
                # Only register input if it's the player's turn to pick
                if ATTACK_BTN.checkForInput(mouse_pos):
                    dmg, battle_msg = process_attack(
                        "Player", "Enemy", False, enemy_defending
                    )
                    enemy_hp -= dmg
                    state = "message"
                    msg_timer = 2000
                elif DEFEND_BTN.checkForInput(mouse_pos):
                    player_defending = True
                    battle_msg = "Player defends!"
                    state = "message"
                    msg_timer = 2000
                elif BREAK_BTN.checkForInput(mouse_pos):
                    dmg, battle_msg = process_attack(
                        "Player", "Enemy", True, enemy_defending
                    )
                    enemy_hp -= dmg
                    state = "message"
                    msg_timer = 2000

        pygame.display.update()
