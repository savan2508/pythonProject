import random

import pygame

# Initialize pygame

pygame.init()

# Set display surface
Window_Width = 945
Window_Height = 600
display_surface = pygame.display.set_mode((Window_Width, Window_Height))
pygame.display.set_caption("Catch the Clown")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
Player_Starting_Lives = 5
Clown_Starting_Velocity = 3
Clown_Acceleration = 0.5

score = 0
player_lives = Player_Starting_Lives
clown_velocity = Clown_Starting_Velocity
clown_dx = random.choice([-1, 1])
clown_dy = random.choice([-1, 1])

# Set colors
Blue = (1, 175, 209)
Yellow = (248, 231, 28)

# Set fonts
font = pygame.font.Font("Franxurter.ttf", 32)

# Set Text
title_text = font.render("Catch the clown", True, Blue)
title_rect = title_text.get_rect()
title_rect.topleft = (50, 10)

score_text = font.render("Score: "+ str(score), True, Yellow)
score_rect = score_text.get_rect()
score_rect.topright = (Window_Width-50, 10)

lives_text = font.render("Player Lives: " + str(player_lives), True, Yellow)
lives_rect = lives_text.get_rect()
lives_rect.topright = (Window_Width - 50, 50)

game_over_text = font.render("GAME-OVER", True, Blue, Yellow)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (Window_Width//2, Window_Height//2)

continue_text = font.render("Click Anywhere to play again", True, Yellow, Blue)
continue_rect = continue_text.get_rect()
continue_rect.center = (Window_Width//2, Window_Height//2 + 64)

# Set sound and music
click_sound = pygame.mixer.Sound("click_sound.wav")
miss_sound = pygame.mixer.Sound("miss_sound.wav")
pygame.mixer.music.load("ctc_background_music.wav")

# Set images
background_image = pygame.image.load("background.png")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)

clown_image = pygame.image.load("clown.png")
clown_rect = clown_image.get_rect()
clown_rect.center = (Window_Width//2, Window_Height//2)

# The main game loop
pygame.mixer.music.play(-1, 0, 0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # A click is made
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            # The clown was clicked
            if clown_rect.collidepoint(mouse_x, mouse_y):
                click_sound.play()
                score += 1
                clown_velocity += Clown_Acceleration

                # Move the clown in the new direction
                previous_dx = clown_dx
                previous_dy = clown_dy
                while previous_dx == clown_dx and previous_dy == clown_dy:
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])

            else:
                miss_sound.play()
                player_lives -= 1

    # Move the clown
    clown_rect.x += clown_dx * clown_velocity
    clown_rect.y += clown_dy * clown_velocity

    # Bounce the clown on the edges of the display
    if clown_rect.left <= 0 or clown_rect.right >= Window_Width:
        clown_dx = -1 * clown_dx

    if clown_rect.top <= 0 or clown_rect.bottom >= Window_Height:
        clown_dy = -1 * clown_dy

    # update the HUD
    score_text = font.render("Score: " + str(score), True, Yellow)
    lives_text = font.render("Lives: " + str(player_lives), True, Blue)

    # Check for the game over
    if player_lives == 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # Pause the game until the player clicks
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            # if the player wants to play again
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = Player_Starting_Lives

                    clown_rect.center = (Window_Width//2, Window_Height//2)
                    clown_velocity = Clown_Starting_Velocity
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])

                    pygame.mixer.music.play(-1, 0, 1)
                    is_paused = False

                # Check to see if the players wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # Blit the background
    display_surface.blit(background_image, background_rect)

    # Update the HUD
    display_surface.blit(title_text, title_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(lives_text, lives_rect)

    # Blit assets
    display_surface.blit(clown_image, clown_rect)

    # update the display and FPS
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
