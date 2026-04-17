import pygame
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font
from core.config import TILESIZE, PLAYER_SPEED
from core.gamedata import gamedata
import math


class Camera:
    """
    Camera class to handle camera movement
    The camera follows the player, keeping them centered on screen
    """
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        """Return a rect moved by the camera offset"""
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        """Return a rect moved by the camera offset"""
        return rect.move(self.camera.topleft)

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


class MapPlayer:
    """
    Player class for the map screen
    Handles movement and animation
    """
    def __init__(self, x, y):
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
        frames = [
            pygame.image.load(f"{path}/{name}_{direction}_stand.png"),
            pygame.image.load(f"{path}/{name}_{direction}_walk1.png"),
            pygame.image.load(f"{path}/{name}_{direction}_walk2.png"),
        ]
        return [
            pygame.transform.scale(img, (self.width, self.height)) for img in frames
        ]

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

    def update(self):
        self.movement()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.animation()
        self.x_change = 0
        self.y_change = 0


def map_screen():
    """
    Map screen with camera system
    Player stays centered, background moves
    """
    # Map dimensions (adjust based on your actual map size)
    MAP_WIDTH = 20 * TILESIZE  # 20 tiles wide
    MAP_HEIGHT = 15 * TILESIZE  # 15 tiles high

    # Create camera
    camera = Camera(MAP_WIDTH, MAP_HEIGHT)

    # Create player at starting position
    player = MapPlayer(10, 7)  # Start at tile (10, 7)

    # Load background/tile (for now using a simple colored background)
    # You can replace this with actual tile loading
    background_color = (50, 150, 50)  # Green grass color

    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Exit map screen

        # Update player
        player.update()

        # Update camera to follow player
        camera.update(player)

        # Clear screen
        SCREEN.fill((30, 30, 30))

        # Draw background (with camera offset)
        # Create a surface for the map
        map_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
        map_surface.fill(background_color)

        # Draw grid lines to show movement (optional, for debugging)
        for x in range(0, MAP_WIDTH, TILESIZE):
            pygame.draw.line(map_surface, (40, 140, 40), (x, 0), (x, MAP_HEIGHT))
        for y in range(0, MAP_HEIGHT, TILESIZE):
            pygame.draw.line(map_surface, (40, 140, 40), (0, y), (MAP_WIDTH, y))

        # Blit map surface with camera offset
        SCREEN.blit(map_surface, camera.camera.topleft)

        # Draw player at center of screen (always)
        player_screen_x = WIN_WIDTH // 2 - player.width // 2
        player_screen_y = WIN_HEIGHT // 2 - player.height // 2
        SCREEN.blit(player.image, (player_screen_x, player_screen_y))

        # Draw UI
        info_text = get_font(20).render("WASD to move | ESC to exit", True, (255, 255, 255))
        SCREEN.blit(info_text, (10, 10))

        # Draw player coordinates
        coord_text = get_font(20).render(f"Pos: ({player.rect.x // TILESIZE}, {player.rect.y // TILESIZE})", True, (255, 255, 255))
        SCREEN.blit(coord_text, (10, 35))

        pygame.display.update()
