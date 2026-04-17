import pygame
import sys
from core.config import *
from core.gamedata import gamedata
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font
from core.character_location import NPC_POSITIONS
from sprites.player import GamePlayer
from sprites.pet import GamePet
from sprites.npc import NPC
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
        self.map_width = 30 * TILESIZE
        self.map_height = 15 * TILESIZE

    def new(self):
        self.playing = True

        # Create camera
        self.camera = Camera(self.map_width, self.map_height)

        # Create player at starting position
        self.player = GamePlayer(10, 7)  # Start at tile (10, 7)

        # Create pet
        self.pet = GamePet(self.player)

        # Create NPCs from positions defined in character_location.py
        self.npcs = []
        for tile_x, tile_y, sprite_path, name in NPC_POSITIONS:
            npc = NPC(tile_x, tile_y, sprite_path, name)
            self.npcs.append(npc)

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

    def check_npc_collision(self, player, npcs, move_dx, move_dy):
        """Check and resolve collision between player and nearby NPCs using pixel-perfect mask collision.
        
        Prevents player movement in collision direction instead of teleporting.
        
        Args:
            player: Player object with rect and mask
            npcs: List of NPC objects with rect and mask
            move_dx: Player's horizontal movement delta
            move_dy: Player's vertical movement delta
            
        Returns:
            True if collision was detected, False otherwise
        """
        collision_detected = False
        
        # Only check NPCs within reasonable distance (optimization)
        # Check NPCs within 2 tiles of player (128 pixels)
        check_distance = TILESIZE * 2
        
        for npc in npcs:
            # Quick distance check before expensive collision detection
            dx = abs(player.rect.centerx - npc.rect.centerx)
            dy = abs(player.rect.centery - npc.rect.centery)
            
            if dx > check_distance or dy > check_distance:
                continue
            
            # First check rect overlap (fast check)
            if not player.rect.colliderect(npc.rect):
                continue
            
            # Then check mask overlap (pixel-perfect check)
            offset_x = npc.rect.x - player.rect.x
            offset_y = npc.rect.y - player.rect.y
            
            if player.mask.overlap(npc.mask, (offset_x, offset_y)):
                collision_detected = True
                # Determine which side the collision is on and prevent movement in that direction
                # Instead of snapping to edge, just revert the movement in that direction
                
                # Check which axis has more overlap
                if dx > dy:
                    # Horizontal collision - revert horizontal movement
                    player.rect.x -= move_dx
                else:
                    # Vertical collision - revert vertical movement
                    player.rect.y -= move_dy
        
        return collision_detected
    
    def update(self):
        # Store player position before movement
        prev_x = self.player.rect.x
        prev_y = self.player.rect.y
        
        self.player.update()
        self.pet.update()
        
        # Calculate movement deltas
        dx = self.player.rect.x - prev_x
        dy = self.player.rect.y - prev_y
        
        # Keep player within map bounds
        self.player.rect.x = max(0, min(self.player.rect.x, self.map_width - self.player.width))
        self.player.rect.y = max(0, min(self.player.rect.y, self.map_height - self.player.height))
        
        # Check NPC collision with movement deltas
        self.check_npc_collision(self.player, self.npcs, dx, dy)
        
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

        # Draw NPCs with camera offset (before player and pet so they appear on top)
        for npc in self.npcs:
            npc.draw(self.screen, self.camera)

        # Draw pet with camera offset
        pet_screen_x = self.pet.rect.x + self.camera.camera.x
        pet_screen_y = self.pet.rect.y + self.camera.camera.y
        self.screen.blit(self.pet.image, (pet_screen_x, pet_screen_y))

        # Draw player with camera offset
        player_screen_x = self.player.rect.x + self.camera.camera.x
        player_screen_y = self.player.rect.y + self.camera.camera.y
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
