import pygame, math
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font
from core.config import TILESIZE, PLAYER_SPEED
from core.gamedata import gamedata
from components.player_movements import MapPlayer

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
