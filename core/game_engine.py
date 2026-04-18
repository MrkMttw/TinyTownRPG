import pygame
import sys
from core.config import *
from core.gamedata import gamedata
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font
from core.npc_location import NPC_POSITIONS
from sprites.player import GamePlayer
from sprites.pet import GamePet
from sprites.npc import NPC
from components.dialogue_box import DialogueBox
from screens.battlefield import battlefield_screen
from components.queue import queue_screen
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
        self.dialogue_box = DialogueBox()

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
        for npc_data in NPC_POSITIONS:
            if len(npc_data) == 4:
                tile_x, tile_y, sprite_path, name = npc_data
                dialogue = "Hello there!"
            else:
                tile_x, tile_y, sprite_path, name, dialogue = npc_data
            npc = NPC(tile_x, tile_y, sprite_path, name, dialogue)
            self.npcs.append(npc)

        # Background color
        self.background_color = (50, 150, 50)  # Green grass color

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.dialogue_box.active:
                    self.playing = False
                # Handle dialogue input first
                if self.dialogue_box.active:
                    result = self.dialogue_box.handle_input(event)
                    if result == "battle":
                        # Trigger battle
                        player_hp = gamedata["player_data"][0].get("HP", 100)
                        enemy_hp = 100
                        battle_ended = False
                        
                        while not battle_ended:
                            action_queue = queue_screen()
                            player_hp, enemy_hp, battle_ended = battlefield_screen(action_queue, player_hp, enemy_hp)
                # Only handle F key for interaction if dialogue is not active
                elif event.key == pygame.K_f:
                    nearby_npc = self.get_nearby_npc()
                    if nearby_npc:
                        self.dialogue_box.start_dialogue(nearby_npc.name, nearby_npc.dialogue)

    def get_nearby_npc(self):
        """Check if player is within 1 tile of any NPC and return that NPC"""
        player_center = self.player.rect.center
        for npc in self.npcs:
            npc_center = npc.rect.center
            distance = math.sqrt((player_center[0] - npc_center[0])**2 + (player_center[1] - npc_center[1])**2)
            if distance <= TILESIZE * 0.5:
                return npc
        return None

    def update(self):
        # Update dialogue box typing animation
        self.dialogue_box.update()
        
        # Only update player and pet if dialogue is not active
        if not self.dialogue_box.active:
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

        # Create renderable objects list for y-based layering
        renderables = [
            {'type': 'npc', 'obj': npc, 'y': npc.rect.bottom} for npc in self.npcs
        ]
        renderables.append({'type': 'pet', 'obj': self.pet, 'y': self.pet.rect.bottom})
        renderables.append({'type': 'player', 'obj': self.player, 'y': self.player.rect.bottom})

        # Sort by y-coordinate (ascending) for proper depth layering
        renderables.sort(key=lambda x: x['y'])

        # Draw sprites in sorted order
        for renderable in renderables:
            obj = renderable['obj']
            screen_x = obj.rect.x + self.camera.camera.x
            screen_y = obj.rect.y + self.camera.camera.y

            if renderable['type'] == 'npc':
                obj.draw(self.screen, self.camera)
            else:
                self.screen.blit(obj.image, (screen_x, screen_y))

        # Draw UI
        info_text = get_font(20).render("WASD to move | F to interact | ESC to exit", True, (255, 255, 255))
        self.screen.blit(info_text, (10, 10))

        coord_text = get_font(20).render(f"Pos: ({self.player.rect.x // TILESIZE}, {self.player.rect.y // TILESIZE})", True, (255, 255, 255))
        self.screen.blit(coord_text, (10, 35))

        # Show interaction prompt when near NPC (only if dialogue is not active)
        nearby_npc = self.get_nearby_npc()
        if nearby_npc and not self.dialogue_box.active:
            prompt_text = get_font(24).render(f"Press F to interact with {nearby_npc.name}", True, (255, 255, 0))
            prompt_rect = prompt_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 50))
            self.screen.blit(prompt_text, prompt_rect)

        # Draw dialogue box if active
        self.dialogue_box.draw(self.screen)

        pygame.display.update()
        self.clock.tick(FPS)

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
