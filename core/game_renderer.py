import pygame
from core.config import *
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font


class GameRenderer:
    """Handles all game rendering and drawing operations
    
    Attributes:
        game: Reference to the Game instance
    """
    
    def __init__(self, game):
        self.game = game
    
    def draw(self):
        # Draw game objects to the screen
        # Clear screen
        self.game.screen.fill((30, 30, 30))

        # Draw background (with camera offset)
        if self.game.map_image is not None:
            # Create a fresh copy of the map image for this frame
            map_surface = self.game.map_image.copy()
        else:
            # Fallback to colored background
            map_surface = pygame.Surface((self.game.map_width, self.game.map_height))
            map_surface.fill((50, 150, 50))

        # Draw grid lines to show movement
        if TILES_VISIBLE == 1:
            for x in range(0, self.game.map_width, TILESIZE):
                pygame.draw.line(map_surface, (40, 140, 40), (x, 0), (x, self.game.map_height))
            for y in range(0, self.game.map_height, TILESIZE):
                pygame.draw.line(map_surface, (40, 140, 40), (0, y), (self.game.map_width, y))

        # Blit map surface with camera offset
        self.game.screen.blit(map_surface, self.game.camera.camera.topleft)

        # Draw structures with camera offset (after background, before NPCs)
        for structure in self.game.structures:
            structure.draw(self.game.screen, self.game.camera)

        # Create renderable objects list for y-based layering
        renderables = [
            {'type': 'npc', 'obj': npc, 'y': npc.rect.bottom} for npc in self.game.npcs
        ]
        renderables.append({'type': 'pet', 'obj': self.game.pet, 'y': self.game.pet.rect.bottom})
        renderables.append({'type': 'player', 'obj': self.game.player, 'y': self.game.player.rect.bottom})

        # Sort by y-coordinate (ascending) for proper depth layering
        renderables.sort(key=lambda x: x['y'])

        # Draw sprites in sorted order
        for renderable in renderables:
            obj = renderable['obj']
            screen_x = obj.rect.x + self.game.camera.camera.x
            screen_y = obj.rect.y + self.game.camera.camera.y

            if renderable['type'] == 'npc':
                obj.draw(self.game.screen, self.game.camera)
            else:
                self.game.screen.blit(obj.image, (screen_x, screen_y))

        # Draw UI
        info_text = get_font(20).render("WASD to move | SHIFT to sprint | F to interact | TAB for inventory | ESC to pause", True, (255, 255, 255))
        self.game.screen.blit(info_text, (10, 10))

        coord_text = get_font(20).render(f"Pos: ({self.game.player.rect.x // TILESIZE}, {self.game.player.rect.y // TILESIZE})", True, (255, 255, 255))
        self.game.screen.blit(coord_text, (10, 35))
        
        # Draw inventory button in bottom middle
        if self.game.inventory_button_image:
            inventory_button_width = 60
            inventory_button_height = 60
            inventory_button_x = (WIN_WIDTH - inventory_button_width) // 2
            inventory_button_y = WIN_HEIGHT - inventory_button_height - 20
            self.game.screen.blit(self.game.inventory_button_image, (inventory_button_x, inventory_button_y))
        else:
            # Fallback to rectangle if image not loaded
            inventory_button_width = 120
            inventory_button_height = 50
            inventory_button_x = (WIN_WIDTH - inventory_button_width) // 2
            inventory_button_y = WIN_HEIGHT - inventory_button_height - 20

            # Draw button background
            pygame.draw.rect(self.game.screen, (100, 100, 150), (inventory_button_x, inventory_button_y, inventory_button_width, inventory_button_height))
            pygame.draw.rect(self.game.screen, (150, 150, 200), (inventory_button_x, inventory_button_y, inventory_button_width, inventory_button_height), 2)

            # Draw button text
            inventory_text = get_font(20).render("Inventory", True, (255, 255, 255))
            inventory_text_rect = inventory_text.get_rect(center=(inventory_button_x + inventory_button_width // 2, inventory_button_y + inventory_button_height // 2))
            self.game.screen.blit(inventory_text, inventory_text_rect)

        # Show interaction prompt when near NPC (only if dialogue is not active)
        nearby_npc = self.game.get_nearby_npc()
        if nearby_npc and not self.game.dialogue_box.active:
            prompt_text = get_font(24).render(f"Press F to interact with {nearby_npc.name}", True, (255, 255, 0))
            prompt_rect = prompt_text.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT - 50))
            self.game.screen.blit(prompt_text, prompt_rect)

        # Draw dialogue box if active
        self.game.dialogue_box.draw(self.game.screen)

        # Draw pet inventory if active
        self.game.pet_inventory.draw(self.game.screen)

        # Draw pause menu if active
        if self.game.pause_menu.active:
            self.game.pause_menu.draw(self.game.screen)

        pygame.display.update()
        self.game.clock.tick(FPS)
