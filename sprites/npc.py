import pygame
from core.config import TILESIZE


class NPC:
    """NPC class for static characters on the map"""
    def __init__(self, tile_x, tile_y, sprite_path, name="NPC", dialogue="Hello there!"):
        self.name = name
        self.dialogue = dialogue
        self.tile_x = tile_x
        self.tile_y = tile_y
        
        # Convert tile position to pixel position
        self.x = tile_x * TILESIZE
        self.y = tile_y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        # Load and scale sprite
        self.image = pygame.image.load(sprite_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        # Create rect for positioning (centered on tile)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x + TILESIZE // 2, self.y + TILESIZE // 2)
        
        # Create mask for pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)
    
    def get_screen_rect(self, camera):
        """Get the screen-space rectangle adjusted by camera offset"""
        return self.rect.move(camera.camera.topleft)
    
    def draw(self, surface, camera):
        """Draw the NPC on the given surface with camera offset"""
        screen_rect = self.get_screen_rect(camera)
        surface.blit(self.image, screen_rect)
