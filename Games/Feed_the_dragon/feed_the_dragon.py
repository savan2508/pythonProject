import random

import pygame

# Initializing the pygame
pygame.init()

# Create a display surface
window_width = 1000
window_height = 400
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Feed the Dragon")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game value
player_starting_life = 5
player_velocity = 15
coin_starting_velocity = 5
coin_acceleration = 0.5
buffer_distance = 100

score = 0
player_lives = player_starting_life
coin_velocity = coin_starting_velocity

# Set color
green = (0, 255, 0)
darkgreen = (10, 50, 10)
white = (255, 255, 255)
black = (0, 0, 0)

# Set text and font
font = pygame.font.Font('AttackGraffiti.ttf', 32)

score_text = font.render("Score: " + str(score), True, green, darkgreen)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

title_text = font.render('Feed the Dragon', True, green, (255, 0, 0))
title_rect = title_text.get_rect()
title_rect.centerx = window_width // 2
title_rect.y = 10

lives_text = font.render('Player Lives: ' + str(player_lives), True, green, black)
lives_rect = lives_text.get_rect()
lives_rect.topright = (window_width - 10, 10)

game_over_text = font.render('Game Over', True, (255, 0, 0), (0, 0, 255))
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (window_width // 2, window_height // 2)

continue_text = font.render("Press any Key to Continue", True, green, (0, 0, 255))
continue_rect = continue_text.get_rect()
continue_rect.center = (window_width // 2, window_height // 2 + 40)

# Loading Assets
# Set music and volume
coin_sound = pygame.mixer.Sound('coin_sound.wav')
miss_sound = pygame.mixer.Sound('miss_sound.wav')
miss_sound.set_volume(.1)
pygame.mixer.music.load('ftd_background_music.wav')

# Set images
player_image = pygame.image.load('dragon_right.png')
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = window_height // 2

coin_image = pygame.image.load('coin.png')
coin_rect = coin_image.get_rect()
coin_rect.x = window_width + buffer_distance
coin_rect.y = random.randint(64, window_height - 32)

# Main game loop:
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check to see if the user wants to move
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.y -= player_velocity
    if keys[pygame.K_DOWN] and player_rect.bottom < window_height:
        player_rect.y += player_velocity

    # Move the coin
    if coin_rect.x < 0:
        player_lives -= 1
        miss_sound.play()
        coin_rect.x = window_width + buffer_distance
        coin_rect.y = random.randint(64, window_height - 32)
    else:
        # Move the coin
        coin_rect.x -= coin_velocity

    # Check the collision with the dragon
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()
        coin_velocity += coin_acceleration
        coin_rect.x = window_width + buffer_distance
        coin_rect.y = random.randint(64, window_height - 32)

    # Update the HUD for the score and lives
    score_text = font.render("Score: " + str(score), True, green, darkgreen)
    lives_text = font.render("Lives: " + str(player_lives), True, green, black)

    # check for the game over
    if player_lives < 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # Pause the game until the player presses the key
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # check if the player wants to play again
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = player_starting_life
                    player_rect.y = window_height // 2
                    coin_velocity = coin_starting_velocity
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                # The player wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # Fill the display
    display_surface.fill(black)

    # Blit the HUD to screen
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, lives_rect)
    pygame.draw.line(display_surface, (0, 0, 255), (0, 64), (window_width, 64), 2)

    # Blit the assets such as dragon and coin
    display_surface.blit(player_image, player_rect)
    display_surface.blit(coin_image, coin_rect)

    # set up the clock
    clock.tick(FPS)

    # update the window(display surface)
    pygame.display.update()

# Quit the pygame
pygame.quit()
