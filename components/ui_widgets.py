"""
Reusable UI widgets for sliders and toggles
"""
import pygame
from core.shared import get_font


def draw_slider(screen, x, y, width, height, value, label):
    """Draw a volume slider
    
    Args:
        screen: Pygame screen surface
        x: X position
        y: Y position
        width: Slider width
        height: Slider height
        value: Current volume value (0.0-1.0)
        label: Label text
        
    Returns:
        Pygame rect for the slider handle
    """
    # Draw label
    label_text = get_font(24).render(f"{label}: {int(value * 100)}%", True, (255, 255, 255))
    screen.blit(label_text, (x, y - 30))

    # Draw slider background
    slider_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (100, 100, 100), slider_rect)
    pygame.draw.rect(screen, (150, 150, 150), slider_rect, 2)

    # Draw slider handle
    handle_x = x + (value * width)
    handle_rect = pygame.Rect(handle_x - 10, y - 5, 20, height + 10)
    pygame.draw.rect(screen, (255, 255, 255), handle_rect)

    return handle_rect


def draw_toggle(screen, x, y, enabled, label):
    """Draw a toggle button for on/off settings
    
    Args:
        screen: Pygame screen surface
        x: X position (leftmost position)
        y: Y position
        enabled: Boolean current state
        label: Label text
        
    Returns:
        Pygame rect for the toggle button
    """
    # Draw label
    label_text = get_font(24).render(label, True, (255, 255, 255))
    screen.blit(label_text, (x, y))

    # Draw toggle button to the right of the label, vertically centered
    text_height = label_text.get_height()
    toggle_y = y + (text_height - 40) // 2
    toggle_rect = pygame.Rect(x + label_text.get_width() + 20, toggle_y, 60, 30)
    color = (0, 200, 0) if enabled else (200, 0, 0)
    pygame.draw.rect(screen, color, toggle_rect)
    pygame.draw.rect(screen, (255, 255, 255), toggle_rect, 2)

    # Draw toggle text
    toggle_text = get_font(20).render("ON" if enabled else "OFF", True, (255, 255, 255))
    toggle_text_rect = toggle_text.get_rect(center=toggle_rect.center)
    screen.blit(toggle_text, toggle_text_rect)

    return toggle_rect
