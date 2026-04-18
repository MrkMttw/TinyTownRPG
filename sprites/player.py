import pygame
from core.config import *
import math
from core.gamedata import gamedata


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
        self.animation_loop = 1

        # Load character based on gamedata
        char_val = gamedata["in_game_data"][0]["CHARACTER"]
        if char_val == 1:
            path = "assets/characters/Girl"
            CHARACTER_NAME = "girl"
        elif char_val == 2:
            path = "assets/characters/Boy"
            CHARACTER_NAME = "boy"

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
        # Load animation frames
        frames = [
            pygame.image.load(f"{path}/{name}_{direction}_stand.png"),
            pygame.image.load(f"{path}/{name}_{direction}_walk1.png"),
            pygame.image.load(f"{path}/{name}_{direction}_walk2.png"),
        ]
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
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.down_animations):
                    # Loop animation
                    self.animation_loop = 1
            self.mask = pygame.mask.from_surface(self.image)

        elif self.facing == "up":
            # Up animation
            if self.y_change == 0:
                # Standing animation
                self.image = self.up_animations[0]
            else:
                # Walking animation
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.up_animations):
                    # Loop animation
                    self.animation_loop = 1
            self.mask = pygame.mask.from_surface(self.image)

        elif self.facing == "left":
            # Left animation
            if self.x_change == 0:
                # Standing animation
                self.image = self.left_animations[0]
            else:
                # Walking animation
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.left_animations):
                    # Loop animation
                    self.animation_loop = 1
            self.mask = pygame.mask.from_surface(self.image)

        elif self.facing == "right":
            # Right animation
            if self.x_change == 0:
                # Standing animation
                self.image = self.right_animations[0]
            else:
                # Walking animation
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.right_animations):
                    # Loop animation
                    self.animation_loop = 1
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

        if keys[pygame.K_a]:
            # Left movement
            self.x_change -= speed
            self.facing = "left"

        if keys[pygame.K_d]:
            # Right movement
            self.x_change += speed
            self.facing = "right"

        if keys[pygame.K_w]:
            # Up movement
            self.y_change -= speed
            self.facing = "up"

        if keys[pygame.K_s]:
            # Down movement
            self.y_change += speed
            self.facing = "down"

    def update(self):
        """
        Update player position and animation
        Args:
            self: Player instance
        Returns:
            None
        """
        # Handle movement
        self.movement()
        # Update position
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        # Update animation
        self.animation()
        # Reset change variables
        self.x_change = 0
        self.y_change = 0
