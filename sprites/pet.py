import pygame
from core.config import *
import math
from core.gamedata import gamedata


class GamePet:
    """Pet class for camera-based game (not using sprite groups)"""
    def __init__(self, player):
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
        else:
            path = "assets/pets/Sausage"
            PET_NAME = "sausage"

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
        frames = [
            pygame.image.load(f"{path}/{name}_{direction}_stand.png"),
            pygame.image.load(f"{path}/{name}_{direction}_walk1.png"),
            pygame.image.load(f"{path}/{name}_{direction}_walk2.png"),
        ]
        return [
            pygame.transform.scale(img, (self.width, self.height)) for img in frames
        ]

    def follow_player(self):
        self.dx = self.player.rect.x - self.pos_x
        self.dy = self.player.rect.y - self.pos_y
        distance = math.sqrt(self.dx**2 + self.dy**2)

        self.is_moving = distance > TILESIZE * 0.5
        if self.is_moving and distance > 0:
            self.pos_x += (self.dx / distance) * PLAYER_SPEED * PET_SPEED
            self.pos_y += (self.dy / distance) * PLAYER_SPEED * PET_SPEED

        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)

        if abs(self.dx) > abs(self.dy):
            self.facing = "right" if self.dx > 0 else "left"
        else:
            self.facing = "down" if self.dy > 0 else "up"

    def animation(self):
        if self.facing == "down":
            if not self.is_moving:
                self.image = self.down_animations[0]
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.down_animations):
                    self.animation_loop = 1

        elif self.facing == "up":
            if not self.is_moving:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.up_animations):
                    self.animation_loop = 1

        elif self.facing == "left":
            if not self.is_moving:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.left_animations):
                    self.animation_loop = 1

        elif self.facing == "right":
            if not self.is_moving:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.right_animations):
                    self.animation_loop = 1

    def update(self):
        self.follow_player()
        self.animation()
