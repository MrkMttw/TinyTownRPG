import pygame
import sys
from core.config import *
from core.gamedata import gamedata
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font
from sprites.player import GamePlayer
from sprites.pet import GamePet
import math


class Camera:
    """Camera class to handle camera movement"""
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def update(self, target):
        """Update camera position to follow target (player)"""
        x = -target.rect.centerx + int(WIN_WIDTH / 2)
        y = -target.rect.centery + int(WIN_HEIGHT / 2)

        # Limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIN_WIDTH), x)  # right
        y = max(-(self.height - WIN_HEIGHT), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        # Map dimensions
        self.map_width = 20 * TILESIZE
        self.map_height = 15 * TILESIZE

    def new(self):
        self.playing = True

        # Create camera
        self.camera = Camera(self.map_width, self.map_height)

        # Create player at starting position
        self.player = GamePlayer(10, 7)  # Start at tile (10, 7)

        # Create pet
        self.pet = GamePet(self.player)

        # Background color
        self.background_color = (50, 150, 50)  # Green grass color

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False

    def update(self):
        self.player.update()
        self.pet.update()
        self.camera.update(self.player)

    def draw(self):
        # Clear screen
        self.screen.fill((30, 30, 30))

        # Draw background (with camera offset)
        map_surface = pygame.Surface((self.map_width, self.map_height))
        map_surface.fill(self.background_color)

        # Draw grid lines to show movement
        for x in range(0, self.map_width, TILESIZE):
            pygame.draw.line(map_surface, (40, 140, 40), (x, 0), (x, self.map_height))
        for y in range(0, self.map_height, TILESIZE):
            pygame.draw.line(map_surface, (40, 140, 40), (0, y), (self.map_width, y))

        # Blit map surface with camera offset
        self.screen.blit(map_surface, self.camera.camera.topleft)

        # Draw pet with camera offset
        pet_screen_x = self.pet.rect.x + self.camera.camera.x
        pet_screen_y = self.pet.rect.y + self.camera.camera.y
        self.screen.blit(self.pet.image, (pet_screen_x, pet_screen_y))

        # Draw player at center of screen
        player_screen_x = WIN_WIDTH // 2 - self.player.width // 2
        player_screen_y = WIN_HEIGHT // 2 - self.player.height // 2
        self.screen.blit(self.player.image, (player_screen_x, player_screen_y))

        # Draw UI
        info_text = get_font(20).render("WASD to move | ESC to exit", True, (255, 255, 255))
        self.screen.blit(info_text, (10, 10))

        coord_text = get_font(20).render(f"Pos: ({self.player.rect.x // TILESIZE}, {self.player.rect.y // TILESIZE})", True, (255, 255, 255))
        self.screen.blit(coord_text, (10, 35))

        pygame.display.update()
        self.clock.tick(FPS)

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
