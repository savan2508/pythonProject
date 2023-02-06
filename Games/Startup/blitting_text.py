import pygame

# initialize a pygame
pygame.init()

# Create a display
window_height = 300
window_width = 600
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Blitting Images!')

# Define color
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
BLACk = (0, 0, 0)


# Define fonts
system_font = pygame.font.SysFont('calibri', 64)
custom_font = pygame.font.Font('AttackGraffiti.ttf', 32)

# Define Text
system_text = system_font.render("Dragons Rule", True, GREEN, DARKGREEN)
system_text_rect = system_text.get_rect()
system_text_rect.center = (window_width/2, window_height/2)

custom_text = custom_font.render("Move the dragon soon!", True, GREEN)
custom_text_rect = custom_text.get_rect()
custom_text_rect.center = (window_width/2, window_height/2 + 100)


# the game loop
run_game = True
while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False

    # Blitting the text surface
    display_surface.blit(system_text, system_text_rect)
    display_surface.blit(custom_text, custom_text_rect)

    # update the display
    pygame.display.update()

# End game
pygame.quit()
