import pygame
from core.shared import WIN_WIDTH, WIN_HEIGHT
from screens.battlefield import battlefield_screen
from components.queue import queue_screen


class GameEvents:
    """Handles all game event processing and input handling
    
    Attributes:
        game: Reference to the Game instance
    """
    
    def __init__(self, game):
        self.game = game
    
    def events(self):
        # Handle game events
        # If pause menu is active, delegate to pause menu event handler
        if self.game.pause_menu.active:
            result = self.game.pause_menu.handle_events()
            if result == "quit":
                self.game.playing = False
                self.game.running = False
            elif result == "settings":
                from screens.settings import show_settings
                show_settings()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.playing = False
                self.game.running = False
            
            # Handle inventory input if active
            if self.game.pet_inventory.active:
                self.game.pet_inventory.handle_input(event)
                continue
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.game.dialogue_box.active and not self.game.pet_inventory.active:
                    self.game.pause_menu.toggle()
                # Handle TAB for inventory (only when not in dialogue or pause menu)
                if event.key == pygame.K_TAB and not self.game.dialogue_box.active and not self.game.pause_menu.active:
                    self.game.pet_inventory.toggle()
                # Handle dialogue input first
                if self.game.dialogue_box.active:
                    result = self.game.dialogue_box.handle_input(event)
                    if result == "battle":
                        # Store the challenged NPC
                        self.game.challenged_npc = self.game.get_nearby_npc()
                        # Trigger battle
                        player_hp = None
                        enemy_hp = None
                        battle_ended = False

                        while not battle_ended:
                            pygame.mixer.stop()  # Stop all sounds including voicelines before queue phase
                            action_queue = queue_screen()
                            player_hp, enemy_hp, battle_ended, exit_to_homescreen = battlefield_screen(action_queue, player_hp, enemy_hp, self.game.challenged_npc)
                            if exit_to_homescreen:
                                # Exit game loop to return to homescreen
                                self.game.playing = False
                                break
                # Only handle F key for interaction if dialogue is not active and not paused
                elif event.key == pygame.K_f and not self.game.pause_menu.active and not self.game.pet_inventory.active:
                    nearby_npc = self.game.get_nearby_npc()
                    if nearby_npc:
                        # Play sound effect if available
                        if nearby_npc.sound_fx_location:
                            try:
                                sound = pygame.mixer.Sound(nearby_npc.sound_fx_location)
                                sound.play()
                            except pygame.error as e:
                                print(f"Error loading sound effect: {e}")
                        self.game.dialogue_box.start_dialogue(nearby_npc.name, nearby_npc.dialogue)
            
            # Handle mouse click for inventory button
            if event.type == pygame.MOUSEBUTTONDOWN and not self.game.dialogue_box.active and not self.game.pause_menu.active:
                if self.game.inventory_button_image:
                    inventory_button_width = 60
                    inventory_button_height = 60
                else:
                    inventory_button_width = 120
                    inventory_button_height = 50
                inventory_button_x = (WIN_WIDTH - inventory_button_width) // 2
                inventory_button_y = WIN_HEIGHT - inventory_button_height - 20
                inventory_button_rect = pygame.Rect(inventory_button_x, inventory_button_y, inventory_button_width, inventory_button_height)

                if inventory_button_rect.collidepoint(event.pos):
                    self.game.pet_inventory.toggle()
