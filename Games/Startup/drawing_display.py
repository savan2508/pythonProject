import pygame

pygame.init()

window_width = 600
window_height = 600
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Drawing Objects')

# Define color as RGB tuples
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Give a background a color to the display
display_surface.fill(RED)

# Draw various shapes on out display
# Line (Surface, color, starting point, ending point, thickness)
pygame.draw.line(display_surface, BLUE, (0, 0), (100, 100), 5)
pygame.draw.line(display_surface, GREEN, (10, 0), (100, 100), 5)

# Circle (surface, color, center, radius, thickness...0 for fill)
pygame.draw.circle(display_surface, CYAN, (300, 300), 100, 6)

# Rectangle(surface, (top-left x, top-left y, wight, height))
pygame.draw.rect(display_surface, MAGENTA, (300, 300, 100, 50))


# The main game loop
run_game = True
while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False

    # update a display
    pygame.display.update()

pygame.quit()