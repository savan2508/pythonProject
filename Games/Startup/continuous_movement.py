import pygame

pygame.init()

# Create a display surface
window_width = 600
window_height = 300
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Continuous Movement')

# Set a motion value
velocity = 5

# load image
dragon_image = pygame.image.load('dragon_right.png')
dragon_rect = dragon_image.get_rect()
dragon_rect.center = (window_width / 2, window_height / 2)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get a list of all the keys that are being held
    keys = pygame.key.get_pressed()

    # Move the dragon continuously
    if keys[pygame.K_LEFT]:
        dragon_rect.x -= velocity
    if keys[pygame.K_RIGHT]:
        dragon_rect.x += velocity
    if keys[pygame.K_UP]:
        dragon_rect.y -= velocity
    if keys[pygame.K_DOWN]:
        dragon_rect.y += velocity

    # fill the display with the background color
    display_surface.fill((0, 0, 0))

    # Blit the image
    display_surface.blit(dragon_image, dragon_rect)

    # Update a display
    pygame.display.update()

# Close the pygame
pygame.quit()
