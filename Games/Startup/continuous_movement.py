import pygame

pygame.init()

# Create a display surface
window_width = 600
window_height = 300
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Continuous Movement with space restriction')

# set FPS and clock
FPS = 60
clock = pygame.time.Clock()

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
    if keys[pygame.K_LEFT] or keys[pygame.K_a] and dragon_rect.x > 0:
        dragon_rect.x -= velocity
    if keys[pygame.K_RIGHT] or keys[pygame.K_d] and dragon_rect.x < window_width:
        dragon_rect.x += velocity
    if keys[pygame.K_UP] or keys[pygame.K_w] and dragon_rect.y > 0:
        dragon_rect.y -= velocity
    if keys[pygame.K_DOWN] or keys[pygame.K_s] and dragon_rect.y < window_height:
        dragon_rect.y += velocity

    # fill the display with the background color
    display_surface.fill((0, 0, 0))

    # Blit the image
    display_surface.blit(dragon_image, dragon_rect)

    # Update a display
    pygame.display.update()

    # Tick the clock
    clock.tick(FPS)

# Close the pygame
pygame.quit()
