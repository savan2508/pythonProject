import pygame

pygame.init()

Window_height = 300
Window_width = 600
display_surface = pygame.display.set_mode((Window_width, Window_height))
pygame.display.set_caption("Adding Sound")

# Load the sound effect
sound_1 = pygame.mixer.Sound('sound_1.wav')
sound_2 = pygame.mixer.Sound('sound_2.wav')

# Play the sound effect
sound_1.play()
pygame.time.delay(2000)
sound_2.play()
pygame.time.delay(2000)

# Change the volume of a sound effect
sound_2.set_volume(.1)
sound_2.play()

# Load background music
pygame.mixer.music.load('music.wav')

# Play the music and stop
pygame.mixer.music.play(-1, 0.0)
pygame.time.delay(1000)
sound_2.play()
pygame.time.delay(5000)
pygame.mixer.music.stop()

# Main game loop
run_game = True
while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False

# End pygame
pygame.quit()
