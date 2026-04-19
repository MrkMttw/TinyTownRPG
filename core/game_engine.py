import pygame
import sys
from core.config import *
from core.gamedata import gamedata
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font
from core.npc_attributes import NPC_ATTRIBUTES
from sprites.player import GamePlayer
from sprites.pet import GamePet
from sprites.npc import NPC
from components.dialogue_box import DialogueBox
from screens.battlefield import battlefield_screen
from components.queue import queue_screen
from components.pause_menu import PauseMenu
from components.pet_inventory import PetInventory
import math


class Camera:
    """Camera class to handle camera movement
    
    Attributes:
        camera: Pygame rectangle representing the camera view
        width: Width of the camera view
        height: Height of the camera view
    """
    def __init__(self, width, height):
        # Initialize camera at position (0, 0)
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def update(self, target):
        # Update camera position to follow target (player)
        x = -target.rect.centerx + int(WIN_WIDTH / 2)
        y = -target.rect.centery + int(WIN_HEIGHT / 2)

        # Limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIN_WIDTH), x)  # right
        y = max(-(self.height - WIN_HEIGHT), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)


class Game:
    """Main game class
    
    Attributes:
        screen: Pygame screen surface
        clock: Pygame clock for frame rate control
        running: Boolean indicating if game is running
        dialogue_box: Dialogue box component
        camera: Camera for scrolling
        player: Player character
        pet: Pet character
        npcs: List of NPC characters
        map_width: Width of the game map
        map_height: Height of the game map
    """

    def __init__(self, screen):
        """
        Initialize the game
        
        Args:
            screen: Pygame screen surface
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.dialogue_box = DialogueBox()
        self.pause_menu = PauseMenu()
        self.pet_inventory = PetInventory(self)
        self.challenged_npc = None  # Store the NPC being challenged

        # Load map image
        try:
            self.map_image = pygame.image.load("assets/maps/map.png").convert_alpha()
            # Scale the map to fit a reasonable game size (30 tiles wide x 15 tiles high)
            target_width = 30 * TILESIZE
            target_height = 15 * TILESIZE
            self.map_image = pygame.transform.scale(self.map_image, (target_width, target_height))
            self.map_width = self.map_image.get_width()
            self.map_height = self.map_image.get_height()
            print(f"Map image loaded and scaled: {self.map_width}x{self.map_height}")
        except pygame.error as e:
            print(f"Error loading map image: {e}")
            # Fallback to colored background
            self.map_width = 30 * TILESIZE
            self.map_height = 15 * TILESIZE
            self.map_image = None

    def new(self):
        """
        Start a new game
        """
        self.playing = True

        # Create camera
        self.camera = Camera(self.map_width, self.map_height)

        # Create player at starting position
        self.player = GamePlayer(10, 7)  # Start at tile (10, 7)

        # Create pet
        self.pet = GamePet(self.player)

        # Create NPCs from positions defined in npc_attributes.py
        self.npcs = []
        for npc_data in NPC_ATTRIBUTES:
            tile_x, tile_y, sprite_path, name, pet, level, sound_fx_location, dialogue = npc_data
            npc = NPC(tile_x, tile_y, sprite_path, name, pet, level, sound_fx_location, dialogue)
            self.npcs.append(npc)

    def events(self):
        # Handle game events
        # If pause menu is active, delegate to pause menu event handler
        if self.pause_menu.active:
            result = self.pause_menu.handle_events()
            if result == "quit":
                self.playing = False
                self.running = False
            elif result == "settings":
                from screens.settings import show_settings
                show_settings()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            
            # Handle inventory input if active
            if self.pet_inventory.active:
                self.pet_inventory.handle_input(event)
                continue
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.dialogue_box.active and not self.pet_inventory.active:
                    self.pause_menu.toggle()
                # Handle TAB for inventory (only when not in dialogue or pause menu)
                if event.key == pygame.K_TAB and not self.dialogue_box.active and not self.pause_menu.active:
                    self.pet_inventory.toggle()
                # Handle dialogue input first
                if self.dialogue_box.active:
                    result = self.dialogue_box.handle_input(event)
                    if result == "battle":
                        # Store the challenged NPC
                        self.challenged_npc = self.get_nearby_npc()
                        # Trigger battle
                        player_hp = None
                        enemy_hp = None
                        battle_ended = False

                        while not battle_ended:
                            action_queue = queue_screen()
                            player_hp, enemy_hp, battle_ended = battlefield_screen(action_queue, player_hp, enemy_hp, self.challenged_npc)
                # Only handle F key for interaction if dialogue is not active and not paused
                elif event.key == pygame.K_f and not self.pause_menu.active and not self.pet_inventory.active:
                    nearby_npc = self.get_nearby_npc()
                    if nearby_npc:
                        # Play sound effect if available
                        if nearby_npc.sound_fx_location:
                            try:
                                sound = pygame.mixer.Sound(nearby_npc.sound_fx_location)
                                sound.play()
                            except pygame.error as e:
                                print(f"Error loading sound effect: {e}")
                        self.dialogue_box.start_dialogue(nearby_npc.name, nearby_npc.dialogue)
            
            # Handle mouse click for inventory button
            if event.type == pygame.MOUSEBUTTONDOWN and not self.dialogue_box.active and not self.pause_menu.active:
                inventory_button_width = 120
                inventory_button_height = 50
                inventory_button_x = (WIN_WIDTH - inventory_button_width) // 2
                inventory_button_y = WIN_HEIGHT - inventory_button_height - 20
                inventory_button_rect = pygame.Rect(inventory_button_x, inventory_button_y, inventory_button_width, inventory_button_height)
                
                if inventory_button_rect.collidepoint(event.pos):
                    self.pet_inventory.toggle()

    def get_nearby_npc(self):
        # Check if player is within 1 tile of any NPC and return that NPC
        player_center = self.player.rect.center
        for npc in self.npcs:
            npc_center = npc.rect.center
            distance = math.sqrt((player_center[0] - npc_center[0])**2 + (player_center[1] - npc_center[1])**2)
            if distance <= TILESIZE * 0.5:
                return npc
        return None
    
    def reload_pet(self):
        """Reload the pet with the currently equipped pet from gamedata"""
        self.pet = GamePet(self.player)

    def update(self):
        # Update game state
        # Update dialogue box typing animation
        self.dialogue_box.update()
        
        # Only update player and pet if dialogue is not active and game is not paused
        if not self.dialogue_box.active and not self.pause_menu.active:
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
        # Draw game objects to the screen
        # Clear screen
        self.screen.fill((30, 30, 30))

        # Draw background (with camera offset)
        if self.map_image is not None:
            # Create a fresh copy of the map image for this frame
            map_surface = self.map_image.copy()
        else:
            # Fallback to colored background
            map_surface = pygame.Surface((self.map_width, self.map_height))
            map_surface.fill((50, 150, 50))

        # Draw grid lines to show movement
        if TILES_VISIBLE == 1:
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
        info_text = get_font(20).render("WASD to move | SHIFT to sprint | F to interact | TAB for inventory | ESC to pause", True, (255, 255, 255))
        self.screen.blit(info_text, (10, 10))

        coord_text = get_font(20).render(f"Pos: ({self.player.rect.x // TILESIZE}, {self.player.rect.y // TILESIZE})", True, (255, 255, 255))
        self.screen.blit(coord_text, (10, 35))
        
        # Draw inventory button in bottom middle
        inventory_button_width = 120
        inventory_button_height = 50
        inventory_button_x = (WIN_WIDTH - inventory_button_width) // 2
        inventory_button_y = WIN_HEIGHT - inventory_button_height - 20
        
        # Draw button background
        pygame.draw.rect(self.screen, (100, 100, 150), (inventory_button_x, inventory_button_y, inventory_button_width, inventory_button_height))
        pygame.draw.rect(self.screen, (150, 150, 200), (inventory_button_x, inventory_button_y, inventory_button_width, inventory_button_height), 2)
        
        # Draw button text
        inventory_text = get_font(20).render("Inventory", True, (255, 255, 255))
        inventory_text_rect = inventory_text.get_rect(center=(inventory_button_x + inventory_button_width // 2, inventory_button_y + inventory_button_height // 2))
        self.screen.blit(inventory_text, inventory_text_rect)

        # Show interaction prompt when near NPC (only if dialogue is not active)
        nearby_npc = self.get_nearby_npc()
        if nearby_npc and not self.dialogue_box.active:
            prompt_text = get_font(24).render(f"Press F to interact with {nearby_npc.name}", True, (255, 255, 0))
            prompt_rect = prompt_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 50))
            self.screen.blit(prompt_text, prompt_rect)

        # Draw dialogue box if active
        self.dialogue_box.draw(self.screen)

        # Draw pet inventory if active
        self.pet_inventory.draw(self.screen)

        # Draw pause menu if active
        if self.pause_menu.active:
            self.pause_menu.draw(self.screen)

        pygame.display.update()
        self.clock.tick(FPS)

    def main(self):
        """
        Main game loop
        """
        while self.playing:
            if self.pause_menu.active:
                # Handle pause menu events
                self.pause_menu.update()
                result = self.pause_menu.handle_events()
                if result == "quit":
                    # Quit to main menu (exit game loop but keep app running)
                    self.playing = False
                elif result == "continue":
                    # Resume game - the toggle was already called in handle_events
                    pass
                elif result == "settings":
                    from screens.settings import settings
                    settings()
                # Draw game state with pause overlay
                self.draw()
            else:
                # Normal game loop
                self.events()
                self.update()
                self.draw()
