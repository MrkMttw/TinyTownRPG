import pygame
from config import *
import math
from gamedata import gamedata

class Pet(pygame.sprite.Sprite):
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self._layer = PLAYER_LAYER - 1  # Draw behind the player
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.width = PET_SIZE
        self.height = PET_SIZE
        
        self.facing = "down"
        self.animation_loop = 1

        # LOAD CHARACTER
        pet_val = gamedata["in_game_data"][0]["PET"]
        if pet_val == 1:
            path = "assets/pets/Sausage"
            PET_NAME = "sausage"

        self.down_animations = self.load_animation_set(path, PET_NAME, "down")
        self.up_animations = self.load_animation_set(path, PET_NAME, "up")
        self.left_animations = self.load_animation_set(path, PET_NAME, "left")
        self.right_animations = self.load_animation_set(path, PET_NAME, "right")

        self.image = self.down_animations[0]
        
        self.rect = self.image.get_rect()
        self.pos_x = float(player.rect.x)
        self.pos_y = float(player.rect.y)
        self.rect.x = int(self.pos_x)
        self.rect.y = int(self.pos_y)
        self.is_moving = False

    def load_animation_set(self, path, name, direction):
        frames = [
            pygame.image.load(f"{path}/{name}_{direction}_stand.png"),
            pygame.image.load(f"{path}/{name}_{direction}_walk1.png"),
            pygame.image.load(f"{path}/{name}_{direction}_walk2.png")
            ]
        return [pygame.transform.scale(img, (self.width, self.height)) for img in frames]

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

    def update(self):
        self.follow_player()
        self.animation()

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
        char_val = gamedata["in_game_data"][0]["CHARACTER"]
        if char_val == 1:
            path = "assets/characters/Girl"
            CHARACTER_NAME = "girl"
        elif char_val == 2:
            path = "assets/characters/Boy"
            CHARACTER_NAME = "boy"
        
        # ANIMATIONS    
        self.down_animations = self.load_animation_set(path, CHARACTER_NAME, "down")
        self.up_animations = self.load_animation_set(path, CHARACTER_NAME, "up")
        self.left_animations = self.load_animation_set(path, CHARACTER_NAME, "left")
        self.right_animations = self.load_animation_set(path, CHARACTER_NAME, "right")
        
        

        self.image = self.down_animations[0]

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    def load_animation_set(self, path, name, direction):
        frames = [
            pygame.image.load(f"{path}/{name}_{direction}_stand.png"),
            pygame.image.load(f"{path}/{name}_{direction}_walk1.png"),
            pygame.image.load(f"{path}/{name}_{direction}_walk2.png")
            ]
        return [pygame.transform.scale(img, (self.width, self.height)) for img in frames]
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