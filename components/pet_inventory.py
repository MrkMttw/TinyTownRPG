import pygame
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font
from core.gamedata import gamedata, update_game_data
from core.battle_loader import get_pet_name


class PetInventory:
    """Pet inventory system for viewing collected pets"""
    
    def __init__(self, game=None):
        self.game = game
        self.active = False
        self.box_width = 800
        self.box_height = 500
        self.box_x = (WIN_WIDTH - self.box_width) // 2
        self.box_y = (WIN_HEIGHT - self.box_height) // 2
        
        # Available pets
        self.all_pets = [
            {"id": 1, "name": "sausage", "display_name": "Sausage"},
            {"id": 2, "name": "bear", "display_name": "Bear"},
            {"id": 3, "name": "germs", "display_name": "Germs"},
            {"id": 4, "name": "pom", "display_name": "Pompoms"},
            {"id": 5, "name": "dino", "display_name": "Dino"},
            {"id": 6, "name": "balls", "display_name": "Balls"},
        ]
        
        # Store pet rectangles for click detection
        self.pet_rects = {}
    
    def toggle(self):
        """Toggle inventory visibility"""
        self.active = not self.active
    
    def handle_input(self, event):
        """Handle keyboard and mouse input for inventory"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE:
                self.toggle()
                return True
        elif event.type == pygame.MOUSEBUTTONDOWN and self.active:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                # Check if any pet rect was clicked
                for pet_id, rect in self.pet_rects.items():
                    if rect.collidepoint(mouse_pos):
                        self.equip_pet(pet_id)
                        return True
        return False
    
    def equip_pet(self, pet_id):
        """Equip a pet by updating gamedata"""
        gamedata["in_game_data"][0]["PET"] = pet_id
        update_game_data()
        # Reload pet in game if game instance is available
        if self.game:
            self.game.reload_pet()
    
    def draw(self, surface):
        """Draw the pet inventory"""
        if not self.active:
            return
        
        # Clear pet rects for this frame
        self.pet_rects = {}
        
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
        
        # Get collected pets and currently equipped pet
        collected_pets = gamedata.get("pets_collected", [])
        equipped_pet_id = gamedata["in_game_data"][0]["PET"]
        
        # Draw pets in grid
        start_y = 80
        pet_size = 100
        gap = 30
        grid_width = 3 * pet_size + 2 * gap  # 3 columns with gaps
        start_x = (self.box_width - grid_width) // 2
        
        for i, pet in enumerate(self.all_pets):
            row = i // 3
            col = i % 3
            
            x = start_x + col * (pet_size + gap)
            y = start_y + row * (pet_size + gap + 30)
            
            # Check if pet is collected
            is_collected = pet["name"] in collected_pets
            is_equipped = pet["id"] == equipped_pet_id
            
            # Draw pet box
            pet_rect = pygame.Rect(x, y, pet_size, pet_size)
            
            # Store pet rect for click detection (only for collected pets)
            if is_collected:
                screen_rect = pygame.Rect(
                    self.box_x + x, 
                    self.box_y + y, 
                    pet_size, 
                    pet_size
                )
                self.pet_rects[pet["id"]] = screen_rect
            
            if is_collected:
                # Use different color for equipped pet
                if is_equipped:
                    pygame.draw.rect(box_surface, (80, 140, 80), pet_rect)
                    pygame.draw.rect(box_surface, (255, 215, 0), pet_rect, 4)  # Gold border for equipped
                else:
                    pygame.draw.rect(box_surface, (50, 100, 50), pet_rect)
                    pygame.draw.rect(box_surface, (100, 200, 100), pet_rect, 2)
                
                # Load and draw pet attack image
                try:
                    pet_image = pygame.image.load(f"assets/battle_actions/{pet['name']}_attack.png")
                    pet_image = pygame.transform.scale(pet_image, (pet_size - 10, pet_size - 10))
                    image_rect = pet_image.get_rect(center=pet_rect.center)
                    box_surface.blit(pet_image, image_rect)
                except pygame.error:
                    # Fallback to colored box if image not found
                    pass
                
                # Draw pet name
                name_font = get_font(20)
                name_color = (255, 215, 0) if is_equipped else (255, 255, 255)
                name_text = name_font.render(pet["display_name"], True, name_color)
                name_rect = name_text.get_rect(center=(pet_rect.centerx, pet_rect.bottom + 20))
                box_surface.blit(name_text, name_rect)
                
                # Draw "EQUIPPED" label if equipped
                if is_equipped:
                    equip_font = get_font(16)
                    equip_text = equip_font.render("EQUIPPED", True, (255, 215, 0))
                    equip_rect = equip_text.get_rect(center=(pet_rect.centerx, pet_rect.top - 12))
                    box_surface.blit(equip_text, equip_rect)
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
        info_text = info_font.render("Press TAB or ESC to close | Click a pet to equip", True, (200, 200, 200))
        info_rect = info_text.get_rect(center=(self.box_width // 2, self.box_height - 30))
        box_surface.blit(info_text, info_rect)
        
        # Blit box to screen
        surface.blit(box_surface, (self.box_x, self.box_y))
