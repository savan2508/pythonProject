import random

import pygame

# Initialize the pygame
pygame.init()

# set the display surface
Window_Width = 800
Window_Height = 600
display_surface = pygame.display.set_mode([Window_Width, Window_Height])
pygame.display.set_caption("Burger Dog")

# Set the FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set the game values
PLAYERS_STARTING_LIVES = 3
PLAYER_NORMAL_VELOCITY = 5
PLAYER_BOOST_VELOCITY = 15
STARTING_BOOST_LEVEL = 100
STARTING_BURGER_VELOCITY = 3
BURGER_ACCELERATION = 0.5
BUFFER_DISTANCE = 100

score = 0
burger_point = 0
burger_eaten = 0

player_lives = PLAYERS_STARTING_LIVES
player_velocity = PLAYER_NORMAL_VELOCITY

boost_level = STARTING_BOOST_LEVEL

burger_velocity = STARTING_BURGER_VELOCITY

# Set Color
Orange = (246, 170, 54)
Black = (0, 0, 0)
White = (255, 255, 255)

# Set fonts
font = pygame.font.Font('WashYourHand.ttf', 32)

# Set Texts
point_text = font.render("Burger Points: " + str(burger_point), True, Orange)
point_rect = point_text.get_rect()
point_rect.topleft = (10, 10)

score_text = font.render("Score: " + str(score), True, Orange)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 50)

title_text = font.render("Burger Dog", True, Orange)
title_rect = title_text.get_rect()
title_rect.centerx = Window_Width // 2
title_rect.y = 10

eaten_text = font.render("Burger Eaten: " + str(burger_eaten), True, Orange)
eaten_rect = eaten_text.get_rect()
eaten_rect.centerx = Window_Width // 2
eaten_rect.y = 50

lives_text = font.render("Live: " + str(player_lives), True, Orange)
lives_rect = lives_text.get_rect()
lives_rect.topright = (Window_Width - 10, 10)

boost_text = font.render("Boost: " + str(boost_level), True, Orange)
boost_rect = boost_text.get_rect()
boost_rect.topright = (Window_Width - 10, 50)

game_over_text = font.render("Final Score: " + str(score), True, Orange)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (Window_Width // 2, Window_Height // 2)

continue_text = font.render("Press any key to continue", True, Orange)
continue_rect = continue_text.get_rect()
continue_rect.center = (Window_Width // 2, Window_Height // 2 + 64)

# Set sound and music
bark_sound = pygame.mixer.Sound('bark_sound.wav')
miss_sound = pygame.mixer.Sound('miss_sound.wav')
pygame.mixer.music.load('bd_background_music.wav')

# Set Images
player_image_right = pygame.image.load("dog_right.png")
player_image_left = pygame.image.load("dog_left.png")
player_image = player_image_left
player_rect = player_image.get_rect()
player_rect.centerx = Window_Width // 2
player_rect.bottom = Window_Height

burger_image = pygame.image.load("burger.png")
burger_rect = burger_image.get_rect()
burger_rect.topleft = (random.randint(0, Window_Width - 32), -BUFFER_DISTANCE)

# The main pygame loop
pygame.mixer.music.play()
running = True
while running:
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= player_velocity
        player_image = player_image_left

    if keys[pygame.K_RIGHT] and player_rect.right < Window_Width:
        player_rect.x += player_velocity
        player_image = player_image_right

    if keys[pygame.K_UP] and player_rect.top > BUFFER_DISTANCE:
        player_rect.y -= player_velocity

    if keys[pygame.K_DOWN] and player_rect.bottom < Window_Height:
        player_rect.y += player_velocity

    # Engage the Boost:
    if keys[pygame.K_SPACE] and boost_level > 0:
        player_velocity = PLAYER_BOOST_VELOCITY
        boost_level -= 1
    else:
        player_velocity = PLAYER_NORMAL_VELOCITY

    # Move the burger and update the points
    burger_rect.y += burger_velocity
    burger_point = int((Window_Height - burger_rect.y + 100) * burger_velocity)

    # player missed the burger
    if burger_rect.y > Window_Height:
        player_lives -= 1
        miss_sound.play()

        burger_rect.topleft = (random.randint(0, Window_Width -32), -BUFFER_DISTANCE)
        burger_velocity = STARTING_BURGER_VELOCITY

        player_rect.centerx = Window_Width // 2
        player_rect.bottom = Window_Height
        boost_level = STARTING_BOOST_LEVEL

    # Check for the collision
    if player_rect.colliderect(burger_rect):
        score += burger_point
        burger_eaten += 1
        bark_sound.play()

        burger_rect.topleft = (random.randint(0, Window_Width - 32), -BUFFER_DISTANCE)
        burger_velocity += BURGER_ACCELERATION

        boost_level += 25
        if boost_level > STARTING_BOOST_LEVEL:
            boost_level = STARTING_BOOST_LEVEL

    # Update the text
    point_text = font.render("Burger Points: " + str(burger_point), True, Orange)
    score_text = font.render("Score: " + str(score), True, Orange)
    eaten_text = font.render("Burger Eaten: " + str(burger_eaten), True, Orange)
    lives_text = font.render("Live: " + str(player_lives), True, Orange)
    boost_text = font.render("Boost: " + str(boost_level), True, Orange)

    # Check for the game over
    if player_lives == 0:
        game_over_text = font.render("Final Score: " + str(score), True, Orange)
        display_surface.blit(game_over_text, game_over_rect)
        continue_text = font.render("Press any key to continue", True, Orange)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()
        is_stopped = True
        pygame.mixer.music.stop()
        while is_stopped:
            for event in pygame.event.get():
                # Check if the player wants to play again
                if event.type == pygame.KEYDOWN:
                    score = 0
                    burger_eaten = 0
                    player_lives = PLAYERS_STARTING_LIVES
                    boost_level = STARTING_BOOST_LEVEL
                    burger_velocity = STARTING_BURGER_VELOCITY

                    pygame.mixer.music.play()
                    is_stopped = False

                if event.type == pygame.QUIT:
                    is_stopped = False
                    running = False

    # Fill the surface
    display_surface.fill(Black)

    # Blit the HUD
    display_surface.blit(point_text, point_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(eaten_text, eaten_rect)
    display_surface.blit(lives_text, lives_rect)
    display_surface.blit(boost_text, boost_rect)
    pygame.draw.line(display_surface, White, (0, 100), (Window_Width, 100), 3)

    # Blit assests
    display_surface.blit(player_image, player_rect)
    display_surface.blit(burger_image, burger_rect)

    # Update the display and tick clock
    pygame.display.update()
    clock.tick(FPS)

# End the pygame
pygame.quit()