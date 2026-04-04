import pygame
import sys
from sprites import Player
from config import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.map_img = pygame.image.load("assets/GameMap.jpg").convert()
        self.map_img = pygame.transform.scale(self.map_img, (WIN_WIDTH, WIN_HEIGHT))

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.player = Player(self, 7, 10)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        # draw background first
        self.screen.blit(self.map_img, (0, 0))

        # draw sprites on top
        self.all_sprites.draw(self.screen)

        pygame.display.update()
        self.clock.tick(FPS)

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def game_over(self):
        pass

    def intro_screen(self):
        pass
