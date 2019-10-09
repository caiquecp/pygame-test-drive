import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

from game import SCREEN_WIDTH, SCREEN_HEIGHT
from game.player import Player
from game.enemy import Enemy

def play():
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    # Create a custom event for adding a new enemy
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 250)

    player = Player()

    # Create groups to hold enemy sprites and all sprites
    # - enemies is used for collision detection and position updates
    enemies = pygame.sprite.Group()
    # - all_sprites is used for rendering
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True

    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
            elif event.type == ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()

        player.update(pressed_keys)

        enemies.update()

        # Fill the background with white
        screen.fill((0, 0, 0))

        # Draw all sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            player.kill()
            running = False

        # Flip the display
        pygame.display.flip()

        # Ensure program maintains a rate of 30 frames per second
        clock.tick(60)

    pygame.quit()