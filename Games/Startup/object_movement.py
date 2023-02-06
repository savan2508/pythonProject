import pygame

pygame.init()

# Create a display board
window_height = 300
window_width = 600
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Discrete movement')

# Set game values
velocity = 10

# Load in images
dragon_image = pygame.image.load('dragon_right.png')
dragon_rect = dragon_image.get_rect()
dragon_rect.centerx = window_width / 2
dragon_rect.bottom = window_height

# The main game loop
run_game = True
while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False

        # Fill the display to erase each dragon after key press
        display_surface.fill((0, 0, 0))

        # Blit assets
        display_surface.blit(dragon_image, dragon_rect)

        # Move based on the mouse clicks:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            dragon_rect.centerx = mouse_x
            dragon_rect.centery = mouse_y

        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]
            dragon_rect.centerx = mouse_x
            dragon_rect.centery = mouse_y

        # Check for the discrete movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dragon_rect.x -= velocity
            if event.key == pygame.K_RIGHT:
                dragon_rect.x += velocity
            if event.key == pygame.K_UP:
                dragon_rect.y -= velocity
            if event.key == pygame.K_DOWN:
                dragon_rect.y += velocity

    # Blit (copy) assets to the screen
    display_surface.blit(dragon_image, dragon_rect)

    # Update a display
    pygame.display.update()

# Pygame quite
pygame.quit()
