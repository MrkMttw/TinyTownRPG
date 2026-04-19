import pygame
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font
from core.gamedata import gamedata
from core.battle_loader import get_pet_name


class PetInventory:
    """Pet inventory system for viewing collected pets"""
    
    def __init__(self):
        self.active = False
        self.box_width = 800
        self.box_height = 500
        self.box_x = (WIN_WIDTH - self.box_width) // 2
        self.box_y = (WIN_HEIGHT - self.box_height) // 2
        
        # Available pets
        self.all_pets = [
            {"id": 1, "name": "sausage", "display_name": "Sausage"},
            {"id": 2, "name": "balls", "display_name": "Balls"},
            {"id": 3, "name": "bear", "display_name": "Bear"},
            {"id": 4, "name": "dino", "display_name": "Dino"},
            {"id": 5, "name": "germs", "display_name": "Germs"},
            {"id": 6, "name": "pom", "display_name": "Pompoms"},
        ]
    
    def toggle(self):
        """Toggle inventory visibility"""
        self.active = not self.active
    
    def handle_input(self, event):
        """Handle keyboard input for inventory"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE:
                self.toggle()
                return True
        return False
    
    def draw(self, surface):
        """Draw the pet inventory"""
        if not self.active:
            return
        
        # Draw semi-transparent background
        overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Draw inventory box
        box_surface = pygame.Surface((self.box_width, self.box_height))
        box_surface.fill((30, 30, 50))
        pygame.draw.rect(box_surface, (100, 100, 150), (0, 0, self.box_width, self.box_height), 3)
        
        # Draw title
        title_font = get_font(32)
        title_text = title_font.render("Pet Inventory", True, (255, 200, 100))
        title_rect = title_text.get_rect(center=(self.box_width // 2, 30))
        box_surface.blit(title_text, title_rect)
        
        # Get collected pets
        collected_pets = gamedata.get("pets_collected", [])
        
        # Draw pets in grid
        start_x = 50
        start_y = 80
        pet_size = 100
        gap = 30
        
        for i, pet in enumerate(self.all_pets):
            row = i // 3
            col = i % 3
            
            x = start_x + col * (pet_size + gap)
            y = start_y + row * (pet_size + gap + 30)
            
            # Check if pet is collected
            is_collected = pet["name"] in collected_pets
            
            # Draw pet box
            pet_rect = pygame.Rect(x, y, pet_size, pet_size)
            if is_collected:
                pygame.draw.rect(box_surface, (50, 100, 50), pet_rect)
                pygame.draw.rect(box_surface, (100, 200, 100), pet_rect, 2)
                
                # Draw pet name
                name_font = get_font(20)
                name_text = name_font.render(pet["display_name"], True, (255, 255, 255))
                name_rect = name_text.get_rect(center=(pet_rect.centerx, pet_rect.bottom + 20))
                box_surface.blit(name_text, name_rect)
            else:
                pygame.draw.rect(box_surface, (50, 50, 50), pet_rect)
                pygame.draw.rect(box_surface, (100, 100, 100), pet_rect, 2)
                
                # Draw lock icon
                lock_font = get_font(40)
                lock_text = lock_font.render("🔒", True, (150, 150, 150))
                lock_rect = lock_text.get_rect(center=pet_rect.center)
                box_surface.blit(lock_text, lock_rect)
                
                # Draw pet name (grayed out)
                name_font = get_font(20)
                name_text = name_font.render("???", True, (150, 150, 150))
                name_rect = name_text.get_rect(center=(pet_rect.centerx, pet_rect.bottom + 20))
                box_surface.blit(name_text, name_rect)
        
        # Draw instructions
        info_font = get_font(18)
        info_text = info_font.render("Press TAB or ESC to close", True, (200, 200, 200))
        info_rect = info_text.get_rect(center=(self.box_width // 2, self.box_height - 30))
        box_surface.blit(info_text, info_rect)
        
        # Blit box to screen
        surface.blit(box_surface, (self.box_x, self.box_y))
