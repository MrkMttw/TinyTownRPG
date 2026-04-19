import pygame
from core.config import *
import math
from core.gamedata import gamedata


class GamePet:
    """
    Pet class for camera-based game (not using sprite groups)
    
    Attributes:
        player: Player instance to follow
        width: Width of the pet
        height: Height of the pet
        facing: Current facing direction
        animation_loop: Animation frame counter
        is_moving: Whether the pet is moving
        down_animations: Down-facing animation frames
        up_animations: Up-facing animation frames
        left_animations: Left-facing animation frames
        right_animations: Right-facing animation frames
        image: Current animation frame
        rect: Rectangle for positioning
        pos_x: X position in pixels
        pos_y: Y position in pixels
        dx: X distance from player
        dy: Y distance from player
    """
    def __init__(self, player):
        """
        Initialize the pet
        
        Args:
            player: Player instance to follow
        """
        self.player = player
        self.width = PET_SIZE
        self.height = PET_SIZE
        self.facing = "down"
        self.animation_loop = 1
        self.is_moving = False

        # Load pet based on gamedata
        pet_val = gamedata["in_game_data"][0]["PET"]
        if pet_val == 1:
            path = "assets/pets/Sausage"
            PET_NAME = "sausage"
        elif pet_val == 2:
            path = "assets/pets/Bear"
            PET_NAME = "bear"
        elif pet_val == 3:
            path = "assets/pets/Germs"
            PET_NAME = "germs"
        elif pet_val == 4:
            path = "assets/pets/Pompoms"
            PET_NAME = "pom"
        elif pet_val == 5:
            path = "assets/pets/Dino"
            PET_NAME = "dino"        
        elif pet_val == 6:
            path = "assets/pets/Balls"
            PET_NAME = "balls"

        # Load animations
        self.down_animations = self.load_animation_set(path, PET_NAME, "down")
        self.up_animations = self.load_animation_set(path, PET_NAME, "up")
        self.left_animations = self.load_animation_set(path, PET_NAME, "left")
        self.right_animations = self.load_animation_set(path, PET_NAME, "right")

        self.image = self.down_animations[0]
        self.rect = self.image.get_rect()

        # Position pet near player
        self.pos_x = float(player.rect.x - TILESIZE)
        self.pos_y = float(player.rect.y)
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

    def load_animation_set(self, path, name, direction):
        """
        Load animation frames for a specific direction
        Args:
            path: Path to animation files
            name: Animation name
            direction: Direction (down, up, left, right)
        Returns:
            List of scaled animation frames
        """
        # Load animation frames
        frames = [
            pygame.image.load(f"{path}/{name}_{direction}_stand.png"),
            pygame.image.load(f"{path}/{name}_{direction}_walk1.png"),
            pygame.image.load(f"{path}/{name}_{direction}_walk2.png"),
        ]
        # Scale frames to pet size
        return [
            pygame.transform.scale(img, (self.width, self.height)) for img in frames
        ]

    def follow_player(self):
        """
        Make the pet follow the player
        Args:
            self: Pet instance
        Returns:
            None
        """
        self.dx = self.player.rect.x - self.pos_x
        self.dy = self.player.rect.y - self.pos_y
        distance = math.sqrt(self.dx**2 + self.dy**2)

        self.is_moving = distance > TILESIZE * 0.5
        if self.is_moving and distance > 0:
            # Move pet towards player
            self.pos_x += (self.dx / distance) * PLAYER_SPEED * PET_SPEED
            self.pos_y += (self.dy / distance) * PLAYER_SPEED * PET_SPEED

        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        if abs(self.dx) > abs(self.dy):
            # Determine horizontal direction
            self.facing = "right" if self.dx > 0 else "left"
        else:
            # Determine vertical direction
            self.facing = "down" if self.dy > 0 else "up"

    def animation(self):
        """
        Handle pet animation based on direction and movement
        Args:
            self: Pet instance
        Returns:
            None
        """
        if self.facing == "down":
            """
            Handle down-facing animation
            """
            if not self.is_moving:
                # Idle animation
                self.image = self.down_animations[0]
            else:
                # Walking animation
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.down_animations):
                    # Loop animation
                    self.animation_loop = 1

        elif self.facing == "up":
            """
            Handle up-facing animation
            """
            if not self.is_moving:
                # Idle animation
                self.image = self.up_animations[0]
            else:
                # Walking animation
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.up_animations):
                    # Loop animation
                    self.animation_loop = 1

        elif self.facing == "left":
            """
            Handle left-facing animation
            """
            if not self.is_moving:
                # Idle animation
                self.image = self.left_animations[0]
            else:
                # Walking animation
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.left_animations):
                    # Loop animation
                    self.animation_loop = 1

        elif self.facing == "right":
            """
            Handle right-facing animation
            """
            if not self.is_moving:
                # Idle animation
                self.image = self.right_animations[0]
            else:
                # Walking animation
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.right_animations):
                    # Loop animation
                    self.animation_loop = 1

    def update(self):
        """
        Update pet position and animation
        Args:
            self: Pet instance
        Returns:
            None
        """
        # Follow player
        self.follow_player()
        # Update animation
        self.animation()
        # Update rect position
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)
