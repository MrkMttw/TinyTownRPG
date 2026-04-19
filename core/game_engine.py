import pygame
import sys
from core.config import *
from core.gamedata import gamedata
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font
from core.npc_attributes import NPC_ATTRIBUTES
from core.structure_location import STRUCTURE_LOCATIONS
from core.structures import Structure
from sprites.player import GamePlayer
from sprites.pet import GamePet
from sprites.npc import NPC
from components.dialogue_box import DialogueBox
from components.pause_menu import PauseMenu
from components.pet_inventory import PetInventory
from core.game_renderer import GameRenderer
from core.game_events import GameEvents
from core.camera import Camera
import math


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
        
        # Initialize renderer and events handlers
        self.renderer = GameRenderer(self)
        self.event_handler = GameEvents(self)

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

        # Load inventory button image
        try:
            self.inventory_button_image = pygame.image.load("assets/inventory.png").convert_alpha()
            # Scale to reasonable button size
            self.inventory_button_image = pygame.transform.scale(self.inventory_button_image, (60, 60))
        except pygame.error as e:
            print(f"Error loading inventory button image: {e}")
            self.inventory_button_image = None

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

        # Create structures from structure_location.py
        self.structures = []
        for tile_x, tile_y, tile_width, tile_height, file_location in STRUCTURE_LOCATIONS:
            structure = Structure(tile_x, tile_y, tile_width, tile_height, file_location)
            self.structures.append(structure)

    def events(self):
        self.event_handler.events()

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
            
            self.player.update(self.structures)
            self.pet.update()
            
            # Calculate movement deltas
            dx = self.player.rect.x - prev_x
            dy = self.player.rect.y - prev_y
            
            # Keep player within map bounds
            self.player.rect.x = max(0, min(self.player.rect.x, self.map_width - self.player.width))
            self.player.rect.y = max(0, min(self.player.rect.y, self.map_height - self.player.height))
            
            self.camera.update(self.player)

    def draw(self):
        self.renderer.draw()

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
