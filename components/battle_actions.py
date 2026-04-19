import pygame
from core.shared import WIN_WIDTH, WIN_HEIGHT, get_font

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