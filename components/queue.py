import pygame
import sys
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font, BUTTON1
from components.button import Button


def queue_screen():
    """
    Queue selection screen - Player selects 3 actions for the upcoming battle rounds.
    Returns a list of 3 actions: "attack", "defend", or "break"

    Attributes:
        action_queue: List of selected actions
        action_names: Dictionary mapping action codes to display names
    """
    action_queue = []
    action_names = {"attack": "ATTACK", "defend": "DEFEND", "break": "BREAK ARMOR"}

    btn_y = WIN_HEIGHT - 100
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

    while len(action_queue) < 3:
        """
        Main game loop for queue selection
        
        Returns:
            list: List of 3 selected actions
        """
        mouse_pos = pygame.mouse.get_pos()
        dt = clock.tick(60)

        # Draw background
        SCREEN.fill((40, 40, 60))

        # Draw title
        title = get_font(50).render("PLAN YOUR 3 TURNS", True, (255, 255, 255))
        title_rect = title.get_rect(center=(WIN_WIDTH // 2, 80))
        SCREEN.blit(title, title_rect)

        # Draw instruction
        instruction = get_font(30).render(f"Select action {len(action_queue) + 1} of 3", True, (200, 200, 200))
        inst_rect = instruction.get_rect(center=(WIN_WIDTH // 2, 150))
        SCREEN.blit(instruction, inst_rect)

        # Draw current queue
        queue_y = 250
        for i, action in enumerate(action_queue):
            text = get_font(35).render(f"Turn {i + 1}: {action_names[action]}", True, (100, 255, 100))
            text_rect = text.get_rect(center=(WIN_WIDTH // 2, queue_y + i * 50))
            SCREEN.blit(text, text_rect)

        # Draw remaining slots
        for i in range(len(action_queue), 3):
            text = get_font(35).render(f"Turn {i + 1}: ...", True, (150, 150, 150))
            text_rect = text.get_rect(center=(WIN_WIDTH // 2, queue_y + i * 50))
            SCREEN.blit(text, text_rect)

        # Draw buttons
        for btn in [ATTACK_BTN, DEFEND_BTN, BREAK_BTN]:
            btn.changeColor(mouse_pos)
            btn.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ATTACK_BTN.checkForInput(mouse_pos):
                    action_queue.append("attack")
                elif DEFEND_BTN.checkForInput(mouse_pos):
                    action_queue.append("defend")
                elif BREAK_BTN.checkForInput(mouse_pos):
                    action_queue.append("break")

        pygame.display.update()

    # Show queue confirmation briefly
    for _ in range(60):  # ~1 second at 60fps
        SCREEN.fill((40, 40, 60))

        confirm = get_font(45).render("QUEUE SET!", True, (100, 255, 100))
        confirm_rect = confirm.get_rect(center=(WIN_WIDTH // 2, 150))
        SCREEN.blit(confirm, confirm_rect)

        queue_y = 250
        for i, action in enumerate(action_queue):
            text = get_font(35).render(f"Turn {i + 1}: {action_names[action]}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIN_WIDTH // 2, queue_y + i * 50))
            SCREEN.blit(text, text_rect)

        pygame.display.update()
        clock.tick(60)

    return action_queue
