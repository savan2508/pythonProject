import random

import pygame

# Initialize the pygame
pygame.init()

vector = pygame.math.Vector2

# Set the display surface (Tile size is 32 * 32 so 1280/32 = 40, 736 /32 = 23 height)
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 736
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Zombie Knight")

# Set the FPS and clock
FPS = 60
clock = pygame.time.Clock()


# Create a function to append the files for the animation
def append_animation(sprite_group, filepath='', filename='', zero=False, extension='.png', image_size=(32, 32),
                     starting_value=1, number_of_files=10, increment=1):
    if not zero:
        for i in range(starting_value, number_of_files + 1, increment):
            sprite_group.append(
                pygame.transform.scale(pygame.image.load(filepath + filename + str(i) + extension), image_size))
    else:
        for i in range(starting_value, number_of_files + 1, increment):
            if i < 10:
                i = '0' + str(i)
            sprite_group.append(
                pygame.transform.scale(pygame.image.load(filepath + filename + i + extension), image_size))


# Define classes
class Game():
    """A class to manage gameplay"""

    def __init__(self, player, zombie_group, platform_group, portal_group, bullet_group, ruby_group):
        """initialize the game"""
        # Set constant variable
        self.STARTING_ROUND_TIME = 30
        self.STARTING_ZOMBIE_CREATION_TIME = 5

        # Set game values
        self.score = 0
        self.round_number = 1
        self.frame_count = 0
        self.round_time = self.STARTING_ROUND_TIME
        self.zombie_creation_time = self.STARTING_ZOMBIE_CREATION_TIME

        # Set Fonts
        self.title_font = pygame.font.Font("fonts/Poultrygeist.ttf", 48)
        self.HUD_font = pygame.font.Font("fonts/Pixel.ttf", 24)

        # Set sounds
        self.lost_ruby_sound = pygame.mixer.Sound("sounds/lost_ruby.wav")
        self.ruby_pickup_sound = pygame.mixer.Sound("sounds/ruby_pickup.wav")
        pygame.mixer.music.load("sounds/level_music.wav")

        # Attach groups and sprites
        self.player = player
        self.zombie_group = zombie_group
        self.platform_group = platform_group
        self.portal_group = portal_group
        self.bullet_group = bullet_group
        self.ruby_group = ruby_group

    def update(self):
        """update the game"""
        # Update the round time every second
        self.frame_count += 1
        if self.frame_count % FPS == 0:
            self.round_time -= 1
            self.frame_count = 0

        # Check for gameplay collisions
        self.check_collisions()

        # Add zombie if the zombie spawn time is met
        self.add_zombie()

        # Check round completion
        self.check_round_completion()
        self.check_game_over()

    def draw(self):
        """Draw the game HUD"""
        # Set colors
        WHITE = (255, 255, 255)
        GREEN = (25, 200, 25)

        # Set Text
        score_text = self.HUD_font.render("Score: " + str(self.score), True, WHITE)
        score_text_rect = score_text.get_rect()
        score_text_rect.topleft = (10, WINDOW_HEIGHT - 50)

        health_text = self.HUD_font.render("Health: " + str(self.player.health), True, WHITE)
        health_text_rect = health_text.get_rect()
        health_text_rect.topleft = (10, WINDOW_HEIGHT - 25)

        title_text = self.title_font.render("Zombie Knight", True, GREEN)
        title_text_rect = title_text.get_rect()
        title_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        round_text = self.HUD_font.render("Night: " + str(self.round_number), True, WHITE)
        round_text_rect = round_text.get_rect()
        round_text_rect.topright = (WINDOW_WIDTH - 10, WINDOW_HEIGHT - 50)

        time_text = self.HUD_font.render("Sunrise In: " + str(self.round_time), True, WHITE)
        time_text_rect = time_text.get_rect()
        time_text_rect.topright = (WINDOW_WIDTH - 10, WINDOW_HEIGHT - 25)

        # Draw the HUD
        display_surface.blit(score_text, score_text_rect)
        display_surface.blit(health_text, health_text_rect)
        display_surface.blit(time_text, time_text_rect)
        display_surface.blit(title_text, title_text_rect)
        display_surface.blit(round_text, round_text_rect)

    def add_zombie(self):
        """Add zombies in the game"""
        # Check to add a zombie every second
        if self.frame_count % FPS == 0:
            # Only add a zombie if zombie creation time has passed
            if self.round_time % self.zombie_creation_time == 0:
                zombie = Zombies(self.platform_group, self.portal_group, self.round_number, 5 + self.round_number)
                self.zombie_group.add(zombie)

    def check_collisions(self):
        """Check collision that affects gameplay"""
        # See if any bullet in the bullet group hit a zombie in the zombie group
        collision_dict = pygame.sprite.groupcollide(self.bullet_group, self.zombie_group, True, False)
        if collision_dict:
            for zombies in collision_dict.values():
                for zombie in zombies:
                    zombie.hit_sound.play()
                    zombie.is_dead = True
                    zombie.animate_death = True

        # See if the player stomped a dead zombie to finish it or collided with a live zombie to take damage
        collide_list = pygame.sprite.spritecollide(self.player, self.zombie_group, False)
        if collide_list:
            for zombie in collide_list:
                # The zombie is dead, stomp it
                if zombie.is_dead:
                    zombie.kick_sound.play()
                    zombie.kill()
                    self.score += 25

                    ruby = Ruby(self.platform_group, self.portal_group)
                    self.ruby_group.add(ruby)

                # The zombie is not dead, player takes damage
                else:
                    self.player.health -= 20
                    self.player.hit_sound.play()
                    self.player.position.x -= 256 * zombie.direction
                    self.player.rect.bottomleft = self.player.position

        # See if a player collided with a ruby
        if pygame.sprite.spritecollide(self.player, self.ruby_group, True):
            self.ruby_pickup_sound.play()
            self.score += 100
            self.player.health += 10
            if self.player.health > self.player.STARTING_HEALTH:
                self.player.health = self.player.STARTING_HEALTH

            # See if a living zombie collide with a ruby
        for zombie in self.zombie_group:
            if not zombie.is_dead:
                if pygame.sprite.spritecollide(zombie, self.ruby_group, True):
                    self.lost_ruby_sound.play()
                    zombie = Zombies(self.platform_group, self.portal_group, self.round_number, 5 + self.round_number)
                    self.zombie_group.add(zombie)

    def check_round_completion(self):
        """Check if the player survived a single night"""
        if self.round_time == 0:
            self.start_new_round()

    def check_game_over(self):
        """Check to see if player lost the game"""
        if self.player.health <= 0:
            pygame.mixer.music.stop()
            self.pause_game("Game Over! Final Score: " + str(self.score),
                            "Press 'Enter' to play again...")
            self.reset_game()

    def start_new_round(self):
        """Start a new round"""
        self.round_number += 1

        # Decrease zombie creation time... more zombies
        if self.round_number < self.STARTING_ZOMBIE_CREATION_TIME:
            self.zombie_creation_time -= 1

        # Reset round values
        self.round_time = self.STARTING_ROUND_TIME

        self.zombie_group.empty()
        self.ruby_group.empty()
        self.bullet_group.empty()

        self.player.reset()

        self.pause_game("You survived the night!", "Press Enter to continue...")

    def pause_game(self, main_text, sub_text):
        """To pause game"""
        global running

        pygame.mixer.music.pause()

        # Set colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GREEN = (25, 200, 25)

        # Create main pause text
        main_text = self.title_font.render(main_text, True, GREEN)
        main_text_rect = main_text.get_rect()
        main_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Create sub text
        sub_text = self.title_font.render(sub_text, True, WHITE)
        sub_text_rect = sub_text.get_rect()
        sub_text_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

        # Display the pause text
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_text_rect)
        display_surface.blit(sub_text, sub_text_rect)
        pygame.display.update()

        # Pause the game until user hits enter or quits
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    # User wants to continue
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                        pygame.mixer.music.unpause()
                # User wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                    pygame.mixer.music.stop()

    def reset_game(self):
        """To reset game"""
        # Reset game values
        self.score = 0
        self.round_number = 1
        self.round_time = self.STARTING_ROUND_TIME
        self.zombie_creation_time = self.STARTING_ZOMBIE_CREATION_TIME

        # Reset the player
        self.player.health = self.player.STARTING_HEALTH
        self.player.reset()

        # Empty sprite groups
        self.zombie_group.empty()
        self.ruby_group.empty()
        self.bullet_group.empty()

        pygame.mixer.music.play(-1, 0.0)


class Tile(pygame.sprite.Sprite):
    """A class to represent a 32x32 pixel area in our display"""

    def __init__(self, x, y, image_int, main_group, sub_group=""):
        """Initialize the tile"""
        super().__init__()
        # Load in the correct image and add it to the correct subgroup
        # Dirt
        if image_int == 1:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (1).png"), (32, 32))
        # Platform tiles
        elif image_int == 2:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (2).png"), (32, 32))
            sub_group.add(self)
        elif image_int == 3:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (3).png"), (32, 32))
            sub_group.add(self)
        elif image_int == 4:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (4).png"), (32, 32))
            sub_group.add(self)
        elif image_int == 5:
            self.image = pygame.transform.scale(pygame.image.load("images/tiles/Tile (5).png"), (32, 32))
            sub_group.add(self)

        # Add every tile to the main group
        main_group.add(self)

        # Get the rect of the image and position within the grid
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Create a mask for better player collisions
        self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
    """A class that the user can control"""

    def __init__(self, x, y, platform_group, portal_group, bullet_group):
        """Initialize the player"""
        super().__init__()

        # Set constant variable
        self.HORIZONTAL_ACCELERATION = 2
        self.HORIZONTAL_FRICTION = 0.15
        self.VERTICAL_ACCELERATION = 0.8  # Gravity
        self.VERTICAL_JUMP_SPEED = 18  # Determine how high the player can jump
        self.STARTING_HEALTH = 100

        # Animation frames
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []
        self.jump_right_sprites = []
        self.jump_left_sprites = []
        self.attack_right_sprites = []
        self.attack_left_sprites = []

        # Moving Animation
        append_animation(self.move_right_sprites,
                         filepath="images/player/run/",
                         filename="Run (",
                         zero=False,
                         extension=").png",
                         image_size=(64, 64),
                         number_of_files=10)

        for sprite in self.move_right_sprites:
            self.move_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # Idling
        append_animation(self.idle_right_sprites,
                         filepath="images/player/idle/",
                         filename="Idle (",
                         zero=False,
                         extension=").png",
                         image_size=(64, 64),
                         number_of_files=10)

        for sprite in self.idle_right_sprites:
            self.idle_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # Jumping Animation
        append_animation(self.jump_right_sprites,
                         filepath="images/player/jump/",
                         filename="Jump (",
                         zero=False,
                         extension=").png",
                         image_size=(64, 64),
                         number_of_files=10)

        for sprite in self.jump_right_sprites:
            self.jump_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # Attack Animation
        append_animation(self.attack_right_sprites,
                         filepath="images/player/attack/",
                         filename="Attack (",
                         zero=False,
                         extension=").png",
                         image_size=(64, 64),
                         number_of_files=10)

        for sprite in self.attack_right_sprites:
            self.attack_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # Load images and get rect
        self.current_sprite = 0
        self.image = self.idle_right_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        # Attach sprite groups
        self.platform_group = platform_group
        self.portal_group = portal_group
        self.bullet_group = bullet_group

        # Animation Booleans
        self.animate_jump = False
        self.animate_fire = False

        # Load sounds
        self.jump_sound = pygame.mixer.Sound("sounds/jump_sound.wav")
        self.slash_sound = pygame.mixer.Sound("sounds/slash_sound.wav")
        self.portal_sound = pygame.mixer.Sound("sounds/portal_sound.wav")
        self.hit_sound = pygame.mixer.Sound("sounds/player_hit.wav")

        # Kinematics vectors
        self.position = vector(x, y)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        # Set initial player values
        self.health = self.STARTING_HEALTH
        self.starting_x = x
        self.starting_y = y

    def update(self):
        """Update the player"""
        self.move()
        self.check_collisions()
        self.check_animations()

        # Update the player mask
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        """Move the player"""
        # Set the acceleration vector
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        # If the user is pressing a key, set the x-component of the acceleration to be no-zero
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, 0.5)
        elif keys[pygame.K_RIGHT]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            self.animate(self.move_right_sprites, 0.5)
        else:
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, 0.5)
            else:
                self.animate(self.idle_left_sprites, 0.5)

        # Calculate new kinematics values
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        # Update rect based on kinematics calculations and add wrap around movement
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        self.rect.bottomleft = self.position

    def check_collisions(self):
        """Check for the collisions with the enemy and portals"""
        # Collision check between player and platforms when falling
        if self.velocity.y > 0:
            collide_platform = pygame.sprite.spritecollide(self, self.platform_group, False, pygame.sprite.collide_mask)
            if collide_platform:
                self.position.y = collide_platform[0].rect.top + 5
                self.velocity.y = 0

        # Collision check between player and platform if jumping up
        if self.velocity.y < 0:
            collide_platform = pygame.sprite.spritecollide(self, self.platform_group, False, pygame.sprite.collide_mask)
            if collide_platform:
                self.velocity.y = 0
                while pygame.sprite.spritecollide(self, self.platform_group, False):
                    self.position.y += 1
                    self.rect.bottomleft = self.position

        # Collision check for portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            # Determine which portal you are colliding with (Left or right)
            if self.position.x > WINDOW_WIDTH // 2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150

            # Top and bottom determination
            if self.position.y > WINDOW_HEIGHT // 2:
                self.position.y = 64
            else:
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position

    def check_animations(self):
        """Check to see if jump/fire animations should run"""
        # Animate the player jump
        if self.animate_jump:
            if self.velocity.x > 0:
                self.animate(self.jump_right_sprites, 0.1)
            else:
                self.animate(self.jump_left_sprites, 0.1)

        # Animate the player attack
        if self.animate_fire:
            if self.velocity.x > 0:
                self.animate(self.attack_right_sprites, 0.25)
            else:
                self.animate(self.attack_left_sprites, 0.25)

    def jump(self):
        """Jump upward if on a platform"""
        # Only jump if on a platform
        if pygame.sprite.spritecollide(self, self.platform_group, False):
            self.jump_sound.play()
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED
            self.animate_jump = True

    def fire(self):
        """Fire a projectile from a sword"""
        self.slash_sound.play()
        Bullet(self.rect.centerx, self.rect.centery, self.bullet_group, self)

    def reset(self):
        """Reset the player"""
        self.velocity = vector(0, 0)
        self.position = vector(self.starting_x, self.starting_y)
        self.rect.bottomleft = self.position

    def animate(self, sprite_list, speed):
        """Animate the player's action"""
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            # End the jump animation
            if self.animate_jump:
                self.animate_jump = False
            # End the attack animation
            if self.animate_fire:
                self.animate_fire = False

        self.image = sprite_list[int(self.current_sprite)]


class Bullet(pygame.sprite.Sprite):
    """A projectile launch by the player from the sword"""

    def __init__(self, x, y, bullet_group, player):
        """Initialize the class"""
        super().__init__()

        # Set constant variable
        self.VELOCITY = 20
        self.RANGE = 500

        # Load image and get rect
        if player.velocity.x > 0:
            self.image = pygame.transform.scale(pygame.image.load("images/player/slash.png"), (32, 32))
        else:
            self.image = pygame.transform.scale(pygame.image.load("images/player/slash.png"), (32, 32))
            self.VELOCITY = -1 * self.VELOCITY

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.starting_x = x

        bullet_group.add(self)

    def update(self):
        """update the bullet"""
        self.rect.x += self.VELOCITY

        # if the bullet has passed the range, kill it
        if abs(self.rect.x - self.starting_x) > self.RANGE:
            self.kill()


class Zombies(pygame.sprite.Sprite):
    """An enemy class that move across the screen"""

    def __init__(self, platform_group, portal_group, min_speed, max_speed):
        """Initialize the zombies"""
        super().__init__()

        # Set constant variable
        self.VERTICAL_ACCELERATION = 3  # Gravity
        self.RISE_TIME = 2

        # Animation frames
        self.walk_right_sprites = []
        self.walk_left_sprites = []
        self.die_right_sprites = []
        self.die_left_sprites = []
        self.rise_right_sprites = []
        self.rise_left_sprites = []

        gender = random.randint(0, 1)
        if gender == 0:  # Boy zombie
            # Walking
            append_animation(sprite_group=self.walk_right_sprites,
                             filepath="images/zombie/boy/walk/",
                             filename="Walk (",
                             extension=").png",
                             image_size=(64, 64))

            for sprite in self.walk_right_sprites:
                self.walk_left_sprites.append(pygame.transform.flip(sprite, True, False))

            # Dying
            append_animation(sprite_group=self.die_right_sprites,
                             filepath="images/zombie/boy/dead/",
                             filename="Dead (",
                             extension=").png",
                             image_size=(64, 64))

            for sprite in self.die_right_sprites:
                self.die_left_sprites.append(pygame.transform.flip(sprite, True, False))

            # Rising
            """Here the append the animation function is used differently from its intended use, the function should 
            increment in positive, but only in this case some values are changed to make it increment reverse"""
            append_animation(sprite_group=self.rise_right_sprites,
                             filepath="images/zombie/boy/walk/",
                             filename="Walk (",
                             starting_value=10,
                             number_of_files=-1,  # This line is an exception to make range(10, 0, -1)
                             extension=").png",
                             image_size=(64, 64),
                             increment=-1)

            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))
        else:  # for girl zombies
            # Walking
            append_animation(sprite_group=self.walk_right_sprites,
                             filepath="images/zombie/girl/walk/",
                             filename="Walk (",
                             extension=").png",
                             image_size=(64, 64))

            for sprite in self.walk_right_sprites:
                self.walk_left_sprites.append(pygame.transform.flip(sprite, True, False))

            # Dying
            append_animation(sprite_group=self.die_right_sprites,
                             filepath="images/zombie/girl/dead/",
                             filename="Dead (",
                             extension=").png",
                             image_size=(64, 64))

            for sprite in self.die_right_sprites:
                self.die_left_sprites.append(pygame.transform.flip(sprite, True, False))

            # Rising
            """Here the append the animation function is used differently from its intended use, the function should 
            increment in positive, but only in this case some values are changed to make it increment reverse"""
            append_animation(sprite_group=self.rise_right_sprites,
                             filepath="images/zombie/girl/walk/",
                             filename="Walk (",
                             starting_value=10,
                             number_of_files=-1,  # This line is an exception to make range(10, 0, -1)
                             extension=").png",
                             image_size=(64, 64),
                             increment=-1)

            for sprite in self.rise_right_sprites:
                self.rise_left_sprites.append(pygame.transform.flip(sprite, True, False))

        # Load an image and get rect
        self.direction = random.choice([-1, 1])

        self.current_sprite = 0
        if self.direction == -1:
            self.image = self.walk_left_sprites[self.current_sprite]
        else:
            self.image = self.walk_right_sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (random.randint(100, WINDOW_WIDTH - 100), -100)

        # Attach sprite groups
        self.platform_group = platform_group
        self.portal_group = portal_group

        # Animation booleans
        self.animate_death = False
        self.animate_rise = False

        # Load Sounds
        self.hit_sound = pygame.mixer.Sound("sounds/zombie_hit.wav")
        self.kick_sound = pygame.mixer.Sound("sounds/zombie_kick.wav")
        self.portal_sound = pygame.mixer.Sound("sounds/portal_sound.wav")

        # Kinematics vectors
        self.position = vector(self.rect.x, self.rect.y)
        self.velocity = vector(self.direction * random.randint(min_speed, max_speed), 0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

        # Initial zombie values
        self.is_dead = False
        self.round_time = 0
        self.frame_count = 0

    def update(self):
        """Update the zombies"""
        self.move()
        self.check_collisions()
        self.check_animations()

        # Determine when the zombie should rise from the dead
        if self.is_dead:
            self.frame_count += 1
            if self.frame_count % FPS == 0:
                self.round_time += 1
                if self.round_time == self.RISE_TIME:
                    self.animate_rise = True
                    # When the zombie died, the image was kept as the last image
                    # When it rises; the zombie animation should start from 0
                    self.current_sprite = 0

    def move(self):
        """Move the zombies"""
        if not self.is_dead:
            if self.direction == -1:
                self.animate(self.walk_left_sprites, 0.5)
            else:
                self.animate(self.walk_right_sprites, 0.5)
            # The acceleration vector does not need to be updated since it is automated
            # Calculate new kinematics values
            self.velocity += self.acceleration
            self.position += self.velocity + 0.5 * self.acceleration

            # Update rect based on kinematics calculations and add wrap around movement
            if self.position.x < 0:
                self.position.x = WINDOW_WIDTH
            elif self.position.x > WINDOW_WIDTH:
                self.position.x = 0

            self.rect.bottomleft = self.position

    def check_collisions(self):
        """Check for the collisions with the enemy and portals"""
        # Collision check between zombie and platforms when falling
        collide_platform = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collide_platform:
            self.position.y = collide_platform[0].rect.top + 1
            self.velocity.y = 0

        # Collision check for portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            # Determine which portal you are colliding with (Left or right)
            if self.position.x > WINDOW_WIDTH // 2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150

            # Top and bottom determination
            if self.position.y > WINDOW_HEIGHT // 2:
                self.position.y = 64
            else:
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position

    def check_animations(self):
        """Check to see if death/rise animations should run"""
        # Animate the zombie death
        if self.animate_death:
            if self.direction == 1:
                self.animate(self.die_right_sprites, 0.095)
            else:
                self.animate(self.die_left_sprites, 0.095)

        # Animate the zombie rise:
        if self.animate_rise:
            if self.direction == 1:
                self.animate(self.rise_right_sprites, 0.095)
            else:
                self.animate(self.rise_left_sprites, 0.095)

    def animate(self, sprite_list, speed):
        """Animate the zombie's action"""
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0
            # End the death animation
            if self.animate_death:
                self.current_sprite = len(sprite_list) - 1
                self.animate_death = False
            # End the rise animation
            if self.animate_rise:
                self.animate_rise = False
                self.is_dead = False
                self.frame_count = 0
                self.round_time = 0

        self.image = sprite_list[int(self.current_sprite)]


class RubyMaker(pygame.sprite.Sprite):
    """A tile is animated, a ruby will be generated here"""

    def __init__(self, x, y, main_group):
        """Initialize the class"""
        super().__init__()
        # Animation frames
        self.ruby_sprites = []

        # Rotating
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile000.png"), (64, 64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile001.png"), (64, 64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile002.png"), (64, 64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile003.png"), (64, 64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile004.png"), (64, 64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile005.png"), (64, 64)))
        self.ruby_sprites.append(pygame.transform.scale(pygame.image.load("images/ruby/tile006.png"), (64, 64)))

        # Load image and get rect
        self.current_sprite = 0
        self.image = self.ruby_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        # Add to the main group for drawing purposes
        main_group.add(self)

    def update(self):
        """Update the ruby maker"""
        self.animate(self.ruby_sprites, .25)

    def animate(self, sprite_list, speed):
        """Animate the ruby maker"""
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]


class Ruby(pygame.sprite.Sprite):
    """A class to player must collect to earn points and health"""

    def __init__(self, platform_group, portal_group):
        """Initialize the ruby"""
        super().__init__()

        # Set constant variable
        self.VERTICAL_ACCELERATION = 3  # Gravity
        self.HORIZONTAL_VELOCITY = 5

        # Animation Frames
        self.ruby_sprites = []

        append_animation(sprite_group=self.ruby_sprites,
                         filepath="images/ruby/",
                         filename="tile0",
                         zero=True,
                         extension=".png",
                         image_size=(64, 64),
                         starting_value=0,
                         number_of_files=6)

        # Load image and get rect
        self.current_sprite = 0
        self.image = self.ruby_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (WINDOW_WIDTH // 2, 100)

        # Attach sprite groups
        self.platform_group = platform_group
        self.portal_group = portal_group

        # Load sounds
        self.portal_sound = pygame.mixer.Sound("sounds/portal_sound.wav")

        # Kinematics vectors
        self.position = vector(self.rect.x, self.rect.y)
        self.velocity = vector(random.choice([-1 * self.HORIZONTAL_VELOCITY, self.HORIZONTAL_VELOCITY]), 0)
        self.acceleration = vector(0, self.VERTICAL_ACCELERATION)

    def update(self):
        """Update the ruby"""
        self.animate(self.ruby_sprites, 0.25)
        self.move()
        self.check_collisions()

    def move(self):
        """Move the ruby"""
        # The acceleration vector does not need to be updated since it is automated
        # Calculate new kinematics values
        self.velocity += self.acceleration
        self.position += self.velocity + 0.5 * self.acceleration

        # Update rect based on kinematics calculations and add wrap around movement
        if self.position.x < 0:
            self.position.x = WINDOW_WIDTH
        elif self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        self.rect.bottomleft = self.position

    def check_collisions(self):
        """Check for the collisions with the platforms and portal"""
        # Collision check between ruby and platforms when falling
        collide_platform = pygame.sprite.spritecollide(self, self.platform_group, False)
        if collide_platform:
            self.position.y = collide_platform[0].rect.top + 1
            self.velocity.y = 0

        # Collision check for portals
        if pygame.sprite.spritecollide(self, self.portal_group, False):
            self.portal_sound.play()
            # Determine which portal you are colliding with (Left or right)
            if self.position.x > WINDOW_WIDTH // 2:
                self.position.x = 86
            else:
                self.position.x = WINDOW_WIDTH - 150

            # Top and bottom determination
            if self.position.y > WINDOW_HEIGHT // 2:
                self.position.y = 64
            else:
                self.position.y = WINDOW_HEIGHT - 132

            self.rect.bottomleft = self.position

    def animate(self, sprite_list, speed):
        """Animate the ruby"""
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]


class Portal(pygame.sprite.Sprite):
    """A Class that if collided with will transport the player"""

    def __init__(self, x, y, color, portal_group):
        """Initialize the class"""
        super().__init__()

        # Animation frames
        self.portal_sprites = []

        # Portal animation
        if color == "green":
            # Green portal
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile000.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile001.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile002.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile003.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile004.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile005.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile006.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile007.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile008.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile009.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile010.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile011.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile012.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile013.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile014.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile015.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile016.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile017.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile018.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile019.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile020.png"), (72, 72)))
            self.portal_sprites.append(
                pygame.transform.scale(pygame.image.load("images/portals/green/tile021.png"), (72, 72)))
        else:
            # Purple Portal
            file_path = "images/portals/purple/tile0"
            for i in range(22):
                if i < 10:
                    i = "0" + str(i)
                portal_sprite = pygame.transform.scale(pygame.image.load(file_path + str(i) + ".png"), (72, 72))
                self.portal_sprites.append(portal_sprite)

        # Load a image and get a rect
        self.current_sprite = random.randint(0, len(self.portal_sprites) - 1)
        self.image = self.portal_sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y)

        # Add to the portal group
        portal_group.add(self)

    def update(self):
        """Update the portal"""
        self.animate(self.portal_sprites, speed=0.2)

    def animate(self, sprite_list, speed):
        """Animate the portal"""
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]


# Create sprite groups
my_main_tile_group = pygame.sprite.Group()
my_platform_group = pygame.sprite.Group()

my_player_group = pygame.sprite.Group()
my_bullet_group = pygame.sprite.Group()

my_zombie_group = pygame.sprite.Group()

my_portal_group = pygame.sprite.Group()
my_ruby_group = pygame.sprite.Group()

# Create tile map
# 0 -> no tile, 1 -> dirt tile, 2-5 -> platforms, 6 -> ruby maker, 7-8 -> portals, 9 -> player
# 23 rows and 40 columns
tile_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     8, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
     4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4,
     4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
     4, 4],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     7, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
     2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
     1, 1]
]

# Generate tile objects from the tile map
# Loop through the 23 lists in the tile map (where i move down of the map)
for i in range(len(tile_map)):
    # Loop through 40 elements in a given list and j moves us across the map
    for j in range(len(tile_map[i])):
        # Dirt tile
        if tile_map[i][j] == 1:
            Tile(j * 32, i * 32, 1, my_main_tile_group)
        elif tile_map[i][j] == 2:
            Tile(j * 32, i * 32, 2, my_main_tile_group, (my_platform_group))
        elif tile_map[i][j] == 3:
            Tile(j * 32, i * 32, 3, my_main_tile_group, (my_platform_group))
        elif tile_map[i][j] == 4:
            Tile(j * 32, i * 32, 4, my_main_tile_group, (my_platform_group))
        elif tile_map[i][j] == 5:
            Tile(j * 32, i * 32, 5, my_main_tile_group, (my_platform_group))
        # Ruby maker
        elif tile_map[i][j] == 6:
            RubyMaker(j * 32, i * 32, my_main_tile_group)
        # Portals
        elif tile_map[i][j] == 7:
            Portal(j * 32, i * 32, "green", my_portal_group)
        elif tile_map[i][j] == 8:
            Portal(j * 32, i * 32, "purple", my_portal_group)
        # Player
        elif tile_map[i][j] == 9:
            my_player = Player(j * 32 - 32, i * 32 + 32, my_platform_group, my_portal_group, my_bullet_group)
            my_player_group.add(my_player)

# Load in a background image
background_image = pygame.transform.scale(pygame.image.load("images/background.png"), (1280, 736))
background_image_rect = background_image.get_rect()
background_image_rect.topleft = (0, 0)

# Create a game
my_game = Game(my_player, my_zombie_group, my_platform_group, my_portal_group, my_bullet_group, my_ruby_group)
my_game.pause_game("Zombie Knight", "Press 'Enter' to Begin")
pygame.mixer.music.play(-1, 0.0)

# The main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Check if player wants to jump
            if event.key == pygame.K_UP:
                my_player.jump()
            # Check if player wants to attack
            if event.key == pygame.K_SPACE:
                my_player.fire()

    # Blit the background image
    display_surface.blit(background_image, background_image_rect)

    # Draw tiles and update ruby maker
    my_main_tile_group.update()
    my_main_tile_group.draw(display_surface)

    # Update and draw the sprite groups
    my_portal_group.update()
    my_portal_group.draw(display_surface)

    my_player_group.update()
    my_player_group.draw(display_surface)

    my_bullet_group.update()
    my_bullet_group.draw(display_surface)

    my_zombie_group.update()
    my_zombie_group.draw(display_surface)

    my_ruby_group.update()
    my_ruby_group.draw(display_surface)

    # Update and draw the game
    my_game.update()
    my_game.draw()

    # Update the display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()
