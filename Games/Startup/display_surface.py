import pygame

# Initialize the pygame
pygame.init()

# Create a display surface and set its caption
window_width = 600
window_height = 300
display_surface = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Hello World')
# The main game loop
run_game = True

while run_game:
    # Loop through a list of Event after occurring
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            run_game = False

pygame.quit()