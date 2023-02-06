import pygame

# initialize game
pygame.init()

# Create a display width
Window_width = 600
Window_height = 300
display_surface = pygame.display.set_mode((Window_width, Window_height))
pygame.display.set_caption("Blitzing Images!")

# Create images. It returns a surface object with the image drawn on it.
dragon_left_image = pygame.image.load('dragon_left.png')
dragon_left_rect = dragon_left_image.get_rect()
dragon_left_rect.topleft = (0, 0)

dragon_right_image = pygame.image.load('dragon_right.png')
dragon_right_rect = dragon_right_image.get_rect()
dragon_right_rect.topright = (Window_width, 0)

# The main game loop
run_game = True
while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False

    # Blit (copy) a surface object at the given coordinates to our display
    display_surface.blit(dragon_left_image, dragon_left_rect)
    display_surface.blit(dragon_right_image, dragon_right_rect)

    pygame.draw.line(display_surface, (255, 255, 255), (0, 75), (Window_width, 75), 4)

    # Update the display
    pygame.display.update()


# End the game
pygame.quit()
