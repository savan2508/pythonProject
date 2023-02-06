import pygame
import random

pygame.init()

# Create a window
window_height = 300
window_width = 600
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Collision detection')

# Set FPS and setup clock
FPS = 60
clock = pygame.time.Clock()

# Set a velocity value for the movement
velocity = 5

# load image
dragon_image = pygame.image.load('dragon_right.png')
dragon_rect = dragon_image.get_rect()
dragon_rect.topleft = (25, 25)

coin_image = pygame.image.load('coin.png')
coin_rect = coin_image.get_rect()
coin_rect.center = (window_width // 2, window_height // 2)


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get a list of all the keys currently pressed down
    keys = pygame.key.get_pressed()

    # following the for loops include the movement to the dragon based on the key pressed.
    if keys[pygame.K_LEFT] and dragon_rect.left > 0:
        dragon_rect.x -= velocity
    if keys[pygame.K_RIGHT] and dragon_rect.right < window_width:
        dragon_rect.x += velocity
    if keys[pygame.K_UP] and dragon_rect.top > 0:
        dragon_rect.y -= velocity
    if keys[pygame.K_DOWN] and dragon_rect.bottom < window_height:
        dragon_rect.y += velocity

    # Fill the surface
    display_surface.fill((0, 0, 0))

    # Draw rectangle to represent each object
    pygame.draw.rect(display_surface, (255, 0, 0), dragon_rect, 1)
    pygame.draw.rect(display_surface, (255, 255, 0), coin_rect, 1)

    # Check for the collision
    if dragon_rect.colliderect(coin_rect):
        print("Hit")
        coin_rect.left = random.randint(0, window_width - 32)
        coin_rect.top = random.randint(0, window_height - 32)

    # Blitz the object
    display_surface.blit(dragon_image, dragon_rect)
    display_surface.blit(coin_image, coin_rect)

    # Update a display
    pygame.display.update()

    # Tick the clock
    clock.tick(FPS)


# Quit the pygame
pygame.quit()