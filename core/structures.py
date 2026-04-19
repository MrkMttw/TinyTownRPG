import pygame
from sprites.buildings import Building
from core.config import TILESIZE


class Structure:
    """
    Structure class for buildings with collision detection
    
    Attributes:
        building: Building instance containing sprite and position data
        tile_x: X position in tiles
        tile_y: Y position in tiles
        tile_width: Width in tiles
        tile_height: Height in tiles
        collision_rect: Rectangle for collision detection
    """
    def __init__(self, tile_x, tile_y, tile_width, tile_height, file_location):
        """
        Initialize the structure
        
        Args:
            tile_x: X position in tiles
            tile_y: Y position in tiles
            tile_width: Width in tiles
            tile_height: Height in tiles
            file_location: Path to structure image
        """
        self.building = Building(tile_x, tile_y, tile_width, tile_height, file_location)
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.tile_width = tile_width
        self.tile_height = tile_height
        
        # Use building's rect for collision to ensure alignment with visual
        self.collision_rect = self.building.rect.copy()
    
    def get_collision_rect(self):
        """
        Get the collision rectangle for this structure
        
        Returns:
            pygame.Rect: Collision rectangle
        """
        return self.collision_rect
    
    def check_collision(self, player_rect):
        """
        Check if player rectangle collides with this structure
        
        Args:
            player_rect: Player's rectangle
            
        Returns:
            bool: True if collision detected, False otherwise
        """
        return self.collision_rect.colliderect(player_rect)
    
    def draw(self, surface, camera):
        """
        Draw the structure on the given surface with camera offset
        
        Args:
            surface: Pygame surface to draw on
            camera: Camera instance
            
        Returns:
            None
        """
        self.building.draw(surface, camera)