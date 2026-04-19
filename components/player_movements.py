import pygame, math
from core.config import TILESIZE, PLAYER_SPEED, SPRINT_MULTIPLIER
from core.gamedata import gamedata


class MapPlayer:
    """
    Player class for the map screen
    Handles movement and animation
    
    Attributes:
        x: X position in pixels
        y: Y position in pixels
        width: Player width
        height: Player height
        x_change: X movement delta
        y_change: Y movement delta
        facing: Current facing direction
        animation_loop: Animation frame counter
        down_animations: Down movement animation frames
        up_animations: Up movement animation frames
        left_animations: Left movement animation frames
        right_animations: Right movement animation frames
        image: Current animation frame
        rect: Player rectangle for collision
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

        self.image = self.down_animations[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def load_animation_set(self, path, name, direction):
        """
        Load animation frames for a specific direction
        
        Args:
            path: Base path to character folder
            name: Character name (girl/boy)
            direction: Movement direction (down/up/left/right)
            
        Returns:
            List of scaled animation frames
        """
        frames = [
            pygame.image.load(f"{path}/{name}_{direction}_stand.png"),
            pygame.image.load(f"{path}/{name}_{direction}_walk1.png"),
            pygame.image.load(f"{path}/{name}_{direction}_walk2.png"),
        ]
        return [
            pygame.transform.scale(img, (self.width, self.height)) for img in frames
        ]

    def animation(self):
        """
        Handle player animation based on movement direction
        Args:
            self: Player instance
        Returns:
            None
        """
        if self.facing == "down":
            if self.y_change == 0:
                # Standing still
                self.image = self.down_animations[0]
            else:
                # Moving
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.down_animations):
                    self.animation_loop = 1

        elif self.facing == "up":
            if self.y_change == 0:
                # Standing still
                self.image = self.up_animations[0]
            else:
                # Moving
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.up_animations):
                    self.animation_loop = 1

        elif self.facing == "left":
            if self.x_change == 0:
                # Standing still
                self.image = self.left_animations[0]
            else:
                # Moving
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.left_animations):
                    self.animation_loop = 1

        elif self.facing == "right":
            if self.x_change == 0:
                # Standing still
                self.image = self.right_animations[0]
            else:
                # Moving
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.right_animations):
                    self.animation_loop = 1

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
            # Moving left
            self.x_change -= speed
            self.facing = "left"

        if keys[pygame.K_d]:
            # Moving right
            self.x_change += speed
            self.facing = "right"

        if keys[pygame.K_w]:
            #Moving up
            self.y_change -= speed
            self.facing = "up"

        if keys[pygame.K_s]:
            #Moving down
            self.y_change += speed
            self.facing = "down"

    def update(self, structures=None):
        """
        Update player position and animation with collision checking
        
        Args:
            self: Player instance
            structures: List of Structure objects to check collision against (default None)
            
        Returns:
            None
        """
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
        else:
            # No structures to check, apply movement normally
            self.rect.x = new_x
            self.rect.y = new_y
        
        self.animation()
        self.x_change = 0
        self.y_change = 0
