import pygame
from core.config import *
import math
from core.gamedata import gamedata
from core.shared import get_font


class GamePlayer:
    """
    Player class for camera-based game (not using sprite groups)
    
    Attributes:
        x: X position in pixels
        y: Y position in pixels
        width: Width of the player
        height: Height of the player
        x_change: X movement amount
        y_change: Y movement amount
        facing: Current facing direction
        animation_loop: Animation frame counter
        down_animations: Down-facing animation frames
        up_animations: Up-facing animation frames
        left_animations: Left-facing animation frames
        right_animations: Right-facing animation frames
        image: Current animation frame
        rect: Rectangle for positioning
        hitbox: Smaller collision hitbox (0.6x tile size)
        mask: Pixel-perfect collision mask
    """
    def __init__(self, x, y):
        """
        Initialize the player
        
        Args:
            x: Starting x position in tiles
            y: Starting y position in tiles
        """
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.x_change = 0
        self.y_change = 0
        self.facing = "down"
        self.animation_loop = 0

        # Load character based on gamedata
        char_val = gamedata["in_game_data"][0]["CHARACTER"]
        if char_val == 1:
            path = "assets/characters/Girl"
            CHARACTER_NAME = "girl"
        elif char_val == 2:
            path = "assets/characters/Boy"
            CHARACTER_NAME = "boy"
        else:
            # Default to Girl if invalid character value
            path = "assets/characters/Girl"
            CHARACTER_NAME = "girl"

        # Load animations
        self.down_animations = self.load_animation_set(path, CHARACTER_NAME, "down")
        self.up_animations = self.load_animation_set(path, CHARACTER_NAME, "up")
        self.left_animations = self.load_animation_set(path, CHARACTER_NAME, "left")
        self.right_animations = self.load_animation_set(path, CHARACTER_NAME, "right")

        # Set initial image and rect
        self.image = self.down_animations[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Create smaller collision hitbox (0.6x of tile size) for tighter collision
        hitbox_size = int(TILESIZE * 0.6)
        self.hitbox = pygame.Rect(0, 0, hitbox_size, hitbox_size)
        self.hitbox.center = self.rect.center
        
        # Create mask for pixel-perfect collision
        self.mask = pygame.mask.from_surface(self.image)

    def load_animation_set(self, path, name, direction):
        """
        Load animation frames for a specific direction
        Args:
            path: Path to character assets
            name: Character name (girl/boy)
            direction: Direction (down/up/left/right)
        Returns:
            List of scaled animation frames
        """
        # Load animation frames with error handling
        frames = []
        for frame_name in ["stand", "walk1", "walk2"]:
            try:
                frame = pygame.image.load(f"{path}/{name}_{direction}_{frame_name}.png")
                frames.append(frame)
            except pygame.error as e:
                print(f"Error loading animation frame {frame_name} for {name} {direction}: {e}")
                # Use a placeholder surface if frame fails to load
                placeholder = pygame.Surface((self.width, self.height))
                placeholder.fill((255, 0, 255))  # Magenta for missing assets
                frames.append(placeholder)
        
        # Scale frames to player size
        return [
            pygame.transform.scale(img, (self.width, self.height)) for img in frames
        ]

    def animation(self):
        """
        Handle player animation based on direction and movement
        Args:
            self: Player instance
        Returns:
            None
        """
        if self.facing == "down":
            # Down animation
            if self.y_change == 0:
                # Standing animation
                self.image = self.down_animations[0]
            else:
                # Walking animation
                self.image = self.down_animations[int(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.down_animations):
                    # Loop animation
                    self.animation_loop = 0
            self.mask = pygame.mask.from_surface(self.image)

        elif self.facing == "up":
            # Up animation
            if self.y_change == 0:
                # Standing animation
                self.image = self.up_animations[0]
            else:
                # Walking animation
                self.image = self.up_animations[int(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.up_animations):
                    # Loop animation
                    self.animation_loop = 0
            self.mask = pygame.mask.from_surface(self.image)

        elif self.facing == "left":
            # Left animation
            if self.x_change == 0:
                # Standing animation
                self.image = self.left_animations[0]
            else:
                # Walking animation
                self.image = self.left_animations[int(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.left_animations):
                    # Loop animation
                    self.animation_loop = 0
            self.mask = pygame.mask.from_surface(self.image)

        elif self.facing == "right":
            # Right animation
            if self.x_change == 0:
                # Standing animation
                self.image = self.right_animations[0]
            else:
                # Walking animation
                self.image = self.right_animations[int(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.right_animations):
                    # Loop animation
                    self.animation_loop = 0
            self.mask = pygame.mask.from_surface(self.image)

    def movement(self):
        """
        Handle player movement based on keyboard input
        Args:
            self: Player instance
        Returns:
            None
        """
        keys = pygame.key.get_pressed()

        # Apply sprint multiplier when shift is held
        speed = PLAYER_SPEED * SPRINT_MULTIPLIER if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else PLAYER_SPEED

        is_moving = False

        if keys[pygame.K_a]:
            # Left movement
            self.x_change -= speed
            self.facing = "left"
            is_moving = True

        if keys[pygame.K_d]:
            # Right movement
            self.x_change += speed
            self.facing = "right"
            is_moving = True

        if keys[pygame.K_w]:
            # Up movement
            self.y_change -= speed
            self.facing = "up"
            is_moving = True

        if keys[pygame.K_s]:
            # Down movement
            self.y_change += speed
            self.facing = "down"
            is_moving = True

    def draw_info_label(self, screen, screen_x, screen_y):
        """
        Draw player name and level above the player sprite
        
        Args:
            screen: Pygame screen surface
            screen_x: Player's screen x position
            screen_y: Player's screen y position
        Returns:
            None
        """
        # Get player data from gamedata
        player_name = gamedata["player_data"][0]["NAME"]
        player_level = gamedata["player_data"][0]["LEVEL"]
        
        # If no name set, use default
        if not player_name:
            player_name = "Player"
        
        # Use game font
        name_font = get_font(18)
        
        # Render name text
        name_text = name_font.render(player_name, True, (255, 255, 255))
        
        # Render level text
        level_text = name_font.render(f"Lvl {player_level}", True, (255, 215, 0))
        
        # Calculate positions (centered above player)
        name_x = screen_x + self.width // 2 - name_text.get_width() // 2
        name_y = screen_y - 25
        level_x = screen_x + self.width // 2 - level_text.get_width() // 2
        level_y = screen_y - 10
        
        # Create semi-transparent black background for name
        bg_width = max(name_text.get_width(), level_text.get_width()) + 10
        bg_height = 35
        bg_x = screen_x + self.width // 2 - bg_width // 2
        bg_y = screen_y - 30
        
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 128))  # Semi-transparent black (alpha = 128)
        screen.blit(bg_surface, (bg_x, bg_y))
        
        # Draw text
        screen.blit(name_text, (name_x, name_y))
        screen.blit(level_text, (level_x, level_y))

    def update(self, structures=None):
        """
        Update player position and animation with collision checking
        Args:
            self: Player instance
            structures: List of Structure objects to check collision against (default None)
        Returns:
            None
        """
        # Handle movement
        self.movement()
        
        # Calculate new position
        new_x = self.rect.x + self.x_change
        new_y = self.rect.y + self.y_change
        
        # Check collision with structures if provided
        if structures:
            # Create a temporary rect for the new position
            temp_rect = self.rect.copy()
            temp_rect.x = new_x
            temp_rect.y = new_y
            
            # Check collision with each structure
            collision_detected = False
            for structure in structures:
                if structure.check_collision(temp_rect):
                    collision_detected = True
                    break
            
            # Only apply movement if no collision
            if not collision_detected:
                self.rect.x = new_x
                self.rect.y = new_y
                # Re-center hitbox on new rect position
                self.hitbox.center = self.rect.center
        else:
            # No structures to check, apply movement normally
            self.rect.x = new_x
            self.rect.y = new_y
        
        # Update animation
        self.animation()
        # Reset change variables
        self.x_change = 0
        self.y_change = 0
