import pygame, math
from core.shared import SCREEN, WIN_WIDTH, WIN_HEIGHT, get_font
from core.config import TILESIZE, PLAYER_SPEED, TILES_VISIBLE
from core.gamedata import gamedata
from core.npc_attributes import NPC_ATTRIBUTES
from core.structure_location import STRUCTURE_LOCATIONS
from sprites.player import GamePlayer
from sprites.npc import NPC
from core.structures import Structure
from core.camera import Camera

def map_screen():
    """
    Map screen with camera system
    Player stays centered, background moves
    """
    # Load map image
    try:
        map_image = pygame.image.load("assets/maps/map.png").convert()
        MAP_WIDTH = map_image.get_width()
        MAP_HEIGHT = map_image.get_height()
        print(f"Map image loaded successfully: {MAP_WIDTH}x{MAP_HEIGHT}")
    except pygame.error as e:
        print(f"Error loading map image: {e}")
        # Fallback to colored background
        MAP_WIDTH = 20 * TILESIZE
        MAP_HEIGHT = 15 * TILESIZE
        map_image = None

    # Create camera
    camera = Camera(MAP_WIDTH, MAP_HEIGHT)

    # Create player at starting position
    player = GamePlayer(10, 7)  # Start at tile (10, 7)

    # Create NPCs from attributes defined in npc_attributes.py
    npcs = []
    for tile_x, tile_y, sprite_path, name, pet, level, sound_fx_location, dialogue in NPC_ATTRIBUTES:
        npc = NPC(tile_x, tile_y, sprite_path, name, pet, level, sound_fx_location, dialogue)
        npcs.append(npc)

    # Create structures from structure_location.py
    structures = []
    for tile_x, tile_y, tile_width, tile_height, file_location in STRUCTURE_LOCATIONS:
        structure = Structure(tile_x, tile_y, tile_width, tile_height, file_location)
        structures.append(structure)

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

        # Update player with structure collision checking
        player.update(structures)

        # Update camera to follow player
        camera.update(player)

        # Clear screen
        SCREEN.fill((30, 30, 30))

        # Draw background (with camera offset)
        if map_image is not None:
            # Create a fresh copy of the map image for this frame
            map_surface = map_image.copy()
        else:
            # Fallback to colored background
            map_surface = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
            map_surface.fill((50, 150, 50))

        # Draw grid lines to show movement (optional, for debugging)
        if TILES_VISIBLE == 1:
            for x in range(0, MAP_WIDTH, TILESIZE):
                pygame.draw.line(map_surface, (40, 140, 40), (x, 0), (x, MAP_HEIGHT))
            for y in range(0, MAP_HEIGHT, TILESIZE):
                pygame.draw.line(map_surface, (40, 140, 40), (0, y), (MAP_WIDTH, y))

        # Blit map surface with camera offset
        SCREEN.blit(map_surface, camera.camera.topleft)

        # Draw structures with camera offset (after background, before NPCs)
        for structure in structures:
            structure.draw(SCREEN, camera)

        # Draw NPCs with camera offset (before player so player appears on top)
        for npc in npcs:
            npc.draw(SCREEN, camera)

        # Draw player at center of screen (always)
        player_screen_x = WIN_WIDTH // 2 - player.width // 2
        player_screen_y = WIN_HEIGHT // 2 - player.height // 2
        SCREEN.blit(player.image, (player_screen_x, player_screen_y))
        
        # Draw player name and level above player
        player.draw_info_label(SCREEN, player_screen_x, player_screen_y)

        # Draw UI
        info_text = get_font(20).render("WASD to move | ESC to pause", True, (255, 255, 255))
        SCREEN.blit(info_text, (10, 10))

        # Draw player coordinates
        coord_text = get_font(20).render(f"Pos: ({player.rect.x // TILESIZE}, {player.rect.y // TILESIZE})", True, (255, 255, 255))
        SCREEN.blit(coord_text, (10, 35))

        # Update display
        pygame.display.update()