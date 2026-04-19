import pygame
from core.config import TILESIZE


class Building:
    """
    Building class for loading and storing building sprites
    
    Attributes:
        file_location: Path to building image
        tile_x: X position in tiles
        tile_y: Y position in tiles
        tile_width: Width in tiles
        tile_height: Height in tiles
        x: X position in pixels
        y: Y position in pixels
        width: Width in pixels
        height: Height in pixels
        image: Scaled building image
        rect: Rectangle for positioning
    """
    def __init__(self, tile_x, tile_y, tile_width, tile_height, file_location):
        """
        Initialize the building
        
        Args:
            tile_x: X position in tiles
            tile_y: Y position in tiles
            tile_width: Width in tiles
            tile_height: Height in tiles
            file_location: Path to building image
        """
        self.file_location = file_location
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.tile_width = tile_width
        self.tile_height = tile_height
        
        # Convert tile position and size to pixels
        self.x = tile_x * TILESIZE
        self.y = tile_y * TILESIZE
        self.width = tile_width * TILESIZE
        self.height = tile_height * TILESIZE
        
        # Load and scale sprite with alpha channel for transparency
        self.image = pygame.image.load(file_location).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        # Create rect for positioning
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
    
    def draw(self, surface, camera):
        """
        Draw the building on the given surface with camera offset
        
        Args:
            surface: Pygame surface to draw on
            camera: Camera instance
            
        Returns:
            None
        """
        # Get screen-space rectangle with camera offset
        screen_rect = self.rect.move(camera.camera.topleft)
        # Draw building on surface
        surface.blit(self.image, screen_rect)