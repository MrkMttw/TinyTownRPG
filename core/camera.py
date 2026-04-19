import pygame
from core.shared import WIN_WIDTH, WIN_HEIGHT


class Camera:
    """
    Camera class to handle camera movement
    The camera follows the player, keeping them centered on screen

    Attributes:
        camera: The camera rectangle
        width: Camera width
        height: Camera height
    """
    def __init__(self, width, height):
        """
        Initialize the camera
        
        Args:
            width: Camera width
            height: Camera height
            
        Returns:
            None
        """
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # Return a rect moved by the camera offset
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        # Return a rect moved by the camera offset
        return rect.move(self.camera.topleft)

    def update(self, target):
        # Update camera position to follow target (player)
        x = -target.rect.centerx + int(WIN_WIDTH / 2)
        y = -target.rect.centery + int(WIN_HEIGHT / 2)

        # Limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIN_WIDTH), x)  # right
        y = max(-(self.height - WIN_HEIGHT), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)
