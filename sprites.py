import pygame
from config import *
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = "down"
        self.animation_loop = 1

        #LOAD CHARACTER
        if CHARACTER == 1:
            path = "assets/characters/Girl"
            CHARACTER_NAME = "girl"
        elif CHARACTER == 2:
            path = "assets/characters/Boy"
            CHARACTER_NAME = "boy"

        #ANIMATIONS
        self.down_animations = [
            pygame.image.load(f"{path}/{CHARACTER_NAME}_down_stand.png"),
            pygame.image.load(f"{path}/{CHARACTER_NAME}_down_walk1.png"),
            pygame.image.load(f"{path}/{CHARACTER_NAME}_down_walk2.png")
        ]

        self.up_animations = [
            pygame.image.load(f"{path}/{CHARACTER_NAME}_up_stand.png"),
            pygame.image.load(f"{path}/{CHARACTER_NAME}_up_walk1.png"),
            pygame.image.load(f"{path}/{CHARACTER_NAME}_up_walk2.png")
        ]

        self.left_animations = [
            pygame.image.load(f"{path}/{CHARACTER_NAME}_left_stand.png"),
            pygame.image.load(f"{path}/{CHARACTER_NAME}_left_walk1.png"),
            pygame.image.load(f"{path}/{CHARACTER_NAME}_left_walk2.png")
        ]

        self.right_animations = [
            pygame.image.load(f"{path}/{CHARACTER_NAME}_right_stand.png"),
            pygame.image.load(f"{path}/{CHARACTER_NAME}_right_walk1.png"),
            pygame.image.load(f"{path}/{CHARACTER_NAME}_right_walk2.png")
        ]
        # scale animations ONCE
        self.down_animations = [pygame.transform.scale(img, (self.width, self.height)) for img in self.down_animations]
        self.up_animations = [pygame.transform.scale(img, (self.width, self.height)) for img in self.up_animations]
        self.left_animations = [pygame.transform.scale(img, (self.width, self.height)) for img in self.left_animations]
        self.right_animations = [pygame.transform.scale(img, (self.width, self.height)) for img in self.right_animations]

        self.image = self.down_animations[0]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def animation(self):
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.down_animations[0]
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.down_animations):
                    self.animation_loop = 1

        elif self.facing == "up":
            if self.y_change == 0:
                self.image = self.up_animations[0]
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.up_animations):
                    self.animation_loop = 1

        elif self.facing == "left":
            if self.x_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.left_animations):
                    self.animation_loop = 1

        elif self.facing == "right":
            if self.x_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.2
                if self.animation_loop >= len(self.right_animations):
                    self.animation_loop = 1

    def update(self):
        self.movement()

        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.animation()

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x_change -= PLAYER_SPEED
            self.facing = "left"

        if keys[pygame.K_d]:
            self.x_change += PLAYER_SPEED
            self.facing = "right"

        if keys[pygame.K_w]:
            self.y_change -= PLAYER_SPEED
            self.facing = "up"

        if keys[pygame.K_s]:
            self.y_change += PLAYER_SPEED
            self.facing = "down"