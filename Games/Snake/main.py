import random

import pygame

# initialize the pygame

pygame.init()

# set up a display window
Window_width = 600
Window_Height = 600
display_surface = pygame.display.set_mode([Window_width, Window_Height])
pygame.display.set_caption("~~Snake~~")

# Set FPS and clock
FPS = 20
clock = pygame.time.Clock()

# Set game values
SNAKE_SIZE = 20

head_x = Window_width // 2
head_y = Window_Height // 2 + 100

snake_dx = 0
snake_dy = 0

score = 0

# Set a color scheme
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
RED = (255, 0, 0)
DARKRED = (150, 0, 0)
WHITE = (255, 255, 255)

# Set fonts
font = pygame.font.SysFont('gabriola', 48)

# Set text
title_text = font.render("~~Snake~~", True, GREEN, DARKRED)
title_rect = title_text.get_rect()
title_rect.center = (Window_width // 2, Window_Height // 2)

score_text = font.render("Score: " + str(score), True, GREEN, DARKRED)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

game_over_text = font.render("GAME OVER", True, RED, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (Window_width // 2, Window_Height // 2)

continue_text = font.render("Press any key to play again", True, RED, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (Window_width // 2, Window_Height // 2 + 64)

# Set Sound and music
pick_up_sound = pygame.mixer.Sound("pick_up_sound.wav")

# Set images (in this case it will be simple rectangles)
# For a rectangle (top-left x, top-left y, width, height)
apple_coord = (500, 500, SNAKE_SIZE, SNAKE_SIZE)
head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)
body_coords = []

apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)
head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)

# The main game loop
running = True

while running:
    # Check if the user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Move the snake
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_dx = -1 * SNAKE_SIZE
                snake_dy = 0

            if event.key == pygame.K_RIGHT:
                snake_dx = SNAKE_SIZE
                snake_dy = 0

            if event.key == pygame.K_UP:
                snake_dx = 0
                snake_dy = SNAKE_SIZE

            if event.key == pygame.K_DOWN:
                snake_dx = 0
                snake_dy = -1 * SNAKE_SIZE

    # Add the head coordinate to the first index of the body coordinate list
    # This will essentially move all the body of the snake by one position
    body_coords.insert(0, head_coord)
    body_coords.pop()

    # Update the position of  the snake head and make a new coordinates
    head_x += snake_dx
    head_y -= snake_dy
    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

    # Check for the game over
    if head_rect.left < 0 or \
            head_rect.right > Window_width or \
            head_rect.bottom > Window_Height or \
            head_rect.top < 0 or \
            head_coord in body_coords:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # Pause the game for the user update and reset the game
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # Check if the player wants to play again
                if event.type == pygame.KEYDOWN:
                    score = 0

                    head_x = Window_width // 2
                    head_y = Window_Height // 2
                    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

                    body_coords = []

                    snake_dx = 0
                    snake_dy = 0

                    is_paused = False

                # if the player wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # Check for the collisions:
    if head_rect.colliderect(apple_rect):
        score += 1
        pick_up_sound.play()

        apple_x = random.randint(0, Window_width - SNAKE_SIZE)
        apple_y = random.randint(0, Window_Height - SNAKE_SIZE)
        apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)

        body_coords.append(head_coord)

    # Update the HUD
    score_text = font.render("Score: " + str(score), True, GREEN, DARKRED)

    # Blit the screen
    display_surface.fill(WHITE)

    # Blit HUD
    display_surface.blit(title_text, title_rect)
    display_surface.blit(score_text, score_rect)

    # Blit assets
    for body in body_coords:
        pygame.draw.rect(display_surface, DARKGREEN, body)
    head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)
    apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

    # update the display and tick clock
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
