import pygame
from core.config import TILESIZE


class NPC:
    """
    NPC class for static characters on the map
    
    Attributes:
        name: NPC name
        dialogue: Default dialogue text
        pet: Pet name
        level: NPC level
        sound_fx_location: Path to sound effect file played on interaction
        tile_x: X position in tiles
        tile_y: Y position in tiles
        x: X position in pixels
        y: Y position in pixels
        width: Width of the NPC
        height: Height of the NPC
        image: NPC sprite image
        rect: Rectangle for positioning
        mask: Pixel-perfect collision mask
    """
    def __init__(self, tile_x, tile_y, sprite_path, name="NPC", pet=None, level=1, sound_fx_location=None, dialogue="Hello there!"):
        """
        Initialize the NPC
        
        Args:
            tile_x: X position in tiles
            tile_y: Y position in tiles
            sprite_path: Path to NPC sprite image
            name: NPC name
            pet: Pet name (e.g., "sausage", "balls")
            level: NPC level
            sound_fx_location: Path to sound effect file played on interaction
            dialogue: Default dialogue text
        """
        self.name = name
        self.dialogue = dialogue
        self.pet = pet
        self.level = level
        self.sound_fx_location = sound_fx_location
        self.sprite_path = sprite_path
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
        """
        Get the screen-space rectangle adjusted by camera offset
        
        Args:
            camera: Camera instance
            
        Returns:
            pygame.Rect: Screen-space rectangle
        """
        return self.rect.move(camera.camera.topleft)
    
    def draw(self, surface, camera, show_info=True):
        """
        Draw the NPC on the given surface with camera offset
        
        Args:
            surface: Pygame surface to draw on
            camera: Camera instance
            show_info: Whether to show name and level above NPC (default True)
            
        Returns:
            None
        """
        # Get screen-space rectangle
        screen_rect = self.get_screen_rect(camera)
        # Draw NPC on surface
        surface.blit(self.image, screen_rect)
        
        # Draw name and level above NPC
        if show_info:
            from core.shared import get_font
            info_text = get_font(18).render(f"{self.name} Lv.{self.level}", True, (255, 255, 255))
            info_rect = info_text.get_rect(midbottom=(screen_rect.centerx, screen_rect.top - 5))
            # Draw semi-transparent background for text
            bg_rect = info_rect.inflate(6, 4)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 128))  # Black with 50% opacity
            surface.blit(bg_surface, bg_rect)
            surface.blit(info_text, info_rect)
