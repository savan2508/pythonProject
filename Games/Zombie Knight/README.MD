# Zombie Knight
Zombie Knight is a thrilling survival game where you take on the role of a knight who must brave the night filled with relentless zombies. Your objective is to survive for as long as possible by fighting off the zombies and avoiding their attacks.

## Gameplay
In Zombie Knight, you control a courageous knight who must navigate through the darkness and confront hordes of zombies. The zombies spawn randomly and move in unpredictable directions. Your task is to stay alive by avoiding collisions with the zombies, as they can deplete your health upon contact.

To defend yourself, you can fire flying swords by pressing the space bar. Aim carefully and time your shots to hit the zombies. When a sword connects with a zombie, it knocks the zombie out for a specific period of time. During this window, you must quickly reach the zombie and stomp on it by touching it, effectively killing it.

After eliminating a zombie, a ruby will spawn from the sky. Your goal is to catch the ruby, as it not only increases your score but also replenishes a portion of your health. Be swift in collecting the rubies to maintain your health and boost your points. However, beware, if a zombie catches the ruby, before you do, a new zombie will spawn from the sky, intensifying the challenge.

As the nights progress, the game becomes increasingly difficult. The zombies become faster and more relentless, posing a greater threat to your survival. Your ultimate objective is to survive for as many nights as possible, showcasing your skills as the formidable Zombie Knight.

## Installation
* To play Zombie Knight on your local machine, follow these steps:

* Download the repository to your local machine. 

* Navigate to the project directory and Install the required dependencies.

* Run the game:
  * You can click on the exe file to run the game directly on your local machine. 
  * You can also run the main.py file in your terminal after changing the directory to the game file. 
  
* Note: Ensure that you have Python and the necessary dependencies installed, such as Pygame, before running the game.

## Controls
* Arrow keys: Move the knight left or right, and up arrow to jump.
* Space bar: Fire a flying sword to attack zombies.

## Code Structure
The code for Zombie Knight follows a modular structure to enhance maintainability and readability. Here is an overview of the code structure:

* The code imports the necessary modules: random for generating random numbers and pygame for the game development framework.

* The Pygame library is initialized using pygame.init().

* The code defines a vector using the pygame.math.Vector2 class. This vector will be used for various calculations in the game.

* The display surface is set using pygame.display.set_mode() with a width of 1280 pixels and a height of 736 pixels. The display surface is the main window where the game will be rendered.

* The window caption is set to "Zombie Knight" using pygame.display.set_caption().

* The Frames Per Second (FPS) is set to 60, and a clock object is created using pygame.time.Clock(). The clock will be used to control the frame rate of the game.

* The code defines a function called append_animation() which is used to load and append animation frames to a sprite group. This function takes several parameters including the sprite group to append the frames, the file path, file name, and other details related to the animation frames.

### Game Class:
The code defines a class called Game which manages the gameplay. The __init__() method initializes the game by setting constant variables, game values, fonts, and sounds. It also attaches groups and sprites to the game object.

#### Methods: 
1. The update() method is responsible for updating the game state. It updates the round time, checks for collisions between game objects, adds zombies to the game, and checks for round completion or game over conditions.

2. The draw() method is responsible for drawing the game HUD (Heads-Up Display) on the display surface. It renders text using predefined fonts and displays information such as score, health, round number, and round time.

3. The add_zombie() method is called to add zombies to the game at regular intervals. It checks the round time and adds a zombie if the zombie creation time has passed.

4. The check_collisions() method checks for various collisions that affect the gameplay. It checks if a bullet hits a zombie, if the player stomps a dead zombie, if the player collides with a live zombie, or if the player collides with a ruby. It handles the appropriate actions for each collision.

5. The check_round_completion() method checks if the player has survived a single night (round). It checks if the round time has reached zero and starts a new round if it has.

6. The check_game_over() method checks if the player has lost the game. It checks if the player's health has reached zero and stops the game, displaying the final score.

7. The start_new_round() method is called to start a new round. It increments the round number, decreases the zombie creation time, resets round values, clears sprite groups, and resets the player.

8. The pause_game() method is called to pause the game and display a pause screen. It takes two text parameters: the main text and sub text to be displayed on the screen. It pauses the game until the user hits the Enter key to continue or quits the game.

9. The reset_game() method is called to reset the game. It resets game values, player health, clears sprite groups, and restarts the game music.

### Tile class:
A class to represent a 32x32 pixel area in the display.

#### Methods:
* __init__(self, x, y, image_int, main_group, sub_group=""): Initializes the tile object.
    ##### Parameters:
    * x: The x-coordinate of the tile's position.
    * y: The y-coordinate of the tile's position.
    * image_int: An integer representing the type of image for the tile.
    * main_group: The main sprite group to which the tile will be added.
    * sub_group: a parameter for the subgroup to which the tile will be added (default: "").
    ##### Functionality:
    * Loads the appropriate image based on the image_int value and scales it to 32x32 pixels.
    * Add the tile object to the specified sprite groups.
    * Creates a collision mask for the tile's image.
  
### Player class:
A class representing the player character that the user can control.

#### Methods:
##### __init__(self, x, y, platform_group, portal_group, bullet_group): Initializes the player object.

    Parameters:
        * x: The initial x-coordinate of the player's position.
        * y: The initial y-coordinate of the player's position.
        * platform_group: The sprite group containing the platforms for collision detection.
        * portal_group: The sprite group containing the portals for collision detection.
        * bullet_group: The sprite group containing the bullets fired by the player.
    Functionality:
        * Sets various constant variables for player movement, acceleration, and health.
        * Loads animation frames for different player actions (e.g., moving, idling, jumping, attacking).
        * Initializes the player's image, position, and other attributes.
        * Attaches the player to the specified sprite groups.
        * Loads sound effects for player actions.
        * Initializes kinematic vectors for player movement.
        * Sets initial player values.

##### update(self): 
Updates the player's state and animations.

    Functionality:
        * Calls other methods to handle player movement, collision detection, and animations.
        * Updates the player's collision mask.

##### move(self): 
Moves the player based on user input and physics.

    Functionality:
        * Sets the acceleration vector based on user input.
        * If the player is moving left or right, sets the acceleration accordingly and animates the appropriate movement sprites.
        * If the player is not moving, applies friction and plays idle animations.
        * Updates the player's position based on kinematic calculations and wraps around the screen if necessary.
        * Updates the player's rect based on the new position.


##### check_collisions(self): 
Checks for collisions with platforms and portals.

    Functionality:
        * Handles collisions between the player and platforms while falling or jumping.
        * Adjusts the player's position and velocity accordingly.
        * Checks for collisions with portals and moves the player to the corresponding location.
        * Updates the player's rect based on the new position.

##### check_animations(self): 
Check if animations (jump and fire) should be played.

    Functionality:
        * Animates the player's jump if the animate_jump flag is set.
        * Animates the player's attack if the animate_fire flag is set.

##### jump(self): 
Makes the player jump if on a platform.

    Functionality:
        * Checks if the player is colliding with a platform.
        * If so, plays the jump sound, sets the vertical velocity, and enables jump animation.

##### fire(self): 
Fires a projectile from the player's sword.

    Functionality:
        * Plays the slash sound effect.
        * Creates a new bullet object at the player's position.

##### reset(self): 
Resets the player's position and attributes.

    Functionality:
        * Resets the player's velocity and position to the starting values.
        * Updates the player's rect based on the new position.

##### animate(self, sprite_list, speed): 
Animates the player's action.

    Parameters:
        * sprite_list: The list of sprites representing the animation frames.
        * speed: The speed at which the animation frames should be cycled.
    Functionality:
        * Animates the player's action by cycling through the sprite list.
        * Updates the current sprite image based on the animation progress.

### Bullet class:
A class representing a projectile launched by the player from their sword.

#### Methods:
##### __init__(self, x, y, bullet_group, player): Initializes the bullet object.

    Parameters:
        x: The initial x-coordinate of the bullet's position.
        y: The initial y-coordinate of the bullet's position.
        bullet_group: The sprite group to which the bullet will be added.
        player: The player object that launched the bullet.
    Functionality:
        Sets constant variables for the bullet's velocity and range.
        Loads the bullet image based on the player's velocity (left or right).
        Sets the bullet's position and starting x-coordinate.
        Adds the bullet object to the specified sprite group.

##### update(self): 
Updates the bullet's position and checks for range limit.

    Functionality:
        Updates the bullet's x-coordinate based on its velocity.
        Checks if the bullet has passed its maximum range from the starting x-coordinate.
        If the bullet has reached the range limit, it is removed from the sprite group.

### Zombies class:
A class representing enemy zombies that move across the screen.

#### Methods:
##### __init__(self, platform_group, portal_group, min_speed, max_speed): 
Initializes the zombie object.

    Parameters:
        platform_group: The sprite group containing the platforms for collision detection.
        portal_group: The sprite group containing the portals for collision detection.
        min_speed: The minimum horizontal speed for the zombies.
        max_speed: The maximum horizontal speed for the zombies.
    Functionality:
        Sets constant variables for vertical acceleration and rise time.
        Loads animation frames for different zombie actions (e.g., walking, dying, rising).
        Determines the gender of the zombie (boy or girl) randomly.
        Loads the appropriate sprites for the zombie's gender and actions.
        Sets the zombie's initial image, direction, and position.
        Attaches the zombie to the specified sprite groups.
        Initializes various attributes and sound effects for the zombie.
        Initializes kinematic vectors for zombie movement.
        Sets initial zombie values.

##### update(self): 
Updates the zombie's state, movement, collisions, and animations.

    Functionality:
        Calls other methods to handle zombie movement, collision detection, and animations.
        Checks if the zombie is dead and updates the frame count and round time.
        If the round time reaches the rise time, enables rise animation and resets relevant attributes.

##### move(self): 
Moves the zombie horizontally and handles animation.

    Functionality:
        Animates the zombie's walking based on its direction (left or right).
        Updates the zombie's position and kinematic values based on its direction.
        Wraps around the screen horizontally if necessary.
        Updates the zombie's rect based on the new position.

##### check_collisions(self): 
Checks for collisions with platforms and portals.

    Functionality:
        Handles collisions between the zombie and platforms while falling.
        Adjusts the zombie's position and velocity accordingly.
        Checks for collisions with portals and moves the zombie to the corresponding location.
        Updates the zombie's rect based on the new position.

##### check_animations(self): 
Checks if death and rise animations should be played.

    Functionality:
        Animates the zombie's death if the animate_death flag is set.
        Animates the zombie's rise if the animate_rise flag is set.

##### animate(self, sprite_list, speed): 
Animates the zombie's action.

    Parameters:
        sprite_list: The list of sprites representing the animation frames.
        speed: The speed at which the animation frames should be cycled.
    Functionality:
        Animates the zombie's action by cycling through the sprite list.
        Updates the current sprite image based on the animation progress.
        Handles the end of the animation cycle and resets relevant attributes if necessary.
        Updates the zombie's image based on the current sprite.

### RubyMaker class:
A class representing a tile that animates and generates a ruby.

#### Methods:
##### __init__(self, x, y, main_group): 
Initializes the RubyMaker object.

    Parameters:
        x: The x-coordinate of the tile's position.
        y: The y-coordinate of the tile's position.
        main_group: The sprite group to which the RubyMaker will be added.
    Functionality:
        Initializes the animation frames for the ruby.
        Loads the image frames for the animation and scales them to a fixed size.
        Sets the initial image frame and rect for the RubyMaker object.
        Sets the position of the RubyMaker object based on the provided coordinates.
        Adds the RubyMaker object to the main group for drawing purposes.

##### update(self): 
Updates the RubyMaker's animation frame.

    Functionality:
        Calls the animate method to update the current animation frame based on the animation speed.

##### animate(self, sprite_list, speed): 
Animate the RubyMaker.

    Parameters:
        sprite_list: The list of sprites representing the animation frames.
        speed: The speed at which the animation frames should be cycled.
    Functionality:
        Increments the current_sprite attribute by the given speed.
        If the current_sprite is beyond the range of the sprite_list, it is reset to 0.
        Updates the RubyMaker's image based on the current_sprite.

### Ruby class:
A class representing a ruby that the player must collect to earn points and health.

#### Methods:

##### __init__(self, platform_group, portal_group): 
Initialize the Ruby object.

    Parameters:
        platform_group: The sprite group containing the platforms for collision detection.
        portal_group: The sprite group containing the portals for collision detection.
    Functionality:
        Sets constant variables for vertical acceleration and horizontal velocity.
        Initializes the animation frames for the ruby.
        Calls the append_animation function to load and append animation frames to the ruby_sprites list.
        Sets the initial image frame and rect for the Ruby object.
        Sets the initial position of the Ruby object.
        Attaches the Ruby object to the specified sprite groups.
        Initializes sound effects and kinematic vectors for the Ruby object.

##### update(self): 
Updates the Ruby's animation frame, movement, and collisions.

    Functionality:
        Calls the animate method to update the current animation frame based on the animation speed.
        Calls the move method to update the Ruby's position based on its kinematic values.
        Calls the check_collisions method to handle collisions with platforms and portals.

##### move(self): 
Moves the Ruby object horizontally and handles wrap-around movement.

    Functionality:
        Updates the Ruby's velocity and position based on its acceleration and previous kinematic values.
        Handles wrap-around movement by resetting the Ruby's x-coordinate if it goes beyond the screen boundaries.
        Updates the Ruby's rect based on the new position.

##### check_collisions(self): 
Checks for collisions with platforms and portals.

    Functionality:
        Checks for collisions between the Ruby and platforms while falling.
        If a collision occurs, adjusts the Ruby's position and velocity to prevent falling through the platform.
        Checks for collisions with portals.
        If a collision occurs, plays a portal sound effect and moves the Ruby to the corresponding location.
        Determines the destination position based on the Ruby's current position and the portal's location.
        Updates the Ruby's rect based on the new position.

##### animate(self, sprite_list, speed): 
Animate the Ruby object.

    Parameters:
        sprite_list: The list of sprites representing the animation frames.
        speed: The speed at which the animation frames should be cycled.
    Functionality:
        Increments the current_sprite attribute by the given speed.
        If the current_sprite is beyond the range of the sprite_list, it is reset to 0.
        Updates the Ruby's image based on the current_sprite.

### Portal class:
The code provided defines a class called Portal, which represents a portal object in a game. The portal is a sprite that, when collided with, transports the player.

* The Portal class is defined as a subclass of pygame.sprite.Sprite, which allows the portal to be used as a sprite in a sprite group.

#### Methods: 

##### init: 
The __init__ method is the constructor of the Portal class. It takes parameters x and y (the position of the portal), color (the color of the portal), and portal_group (the sprite group the portal belongs to). The method initializes the class by calling the constructor of the superclass and setting up the portal's attributes.

* The portal_sprites attribute is a list that will store the animation frames for the portal.

* Based on the color specified in the constructor, the appropriate set of portal sprites is loaded into portal_sprites. If the color is "green," a set of green portal sprites is loaded. Otherwise, if the color is "purple," a set of purple portal sprites is loaded.

* The current sprite for the portal is selected randomly from portal_sprites, and its image and rect attributes are set accordingly.

* The portal is added to the portal_group a sprite group.

##### update:
The update method is responsible for updating the portal. Currently, it calls the animate method to animate the portal using the portal_sprites list and a speed of 0.2.

##### animate: 
The animate method is used to cycle through the portal sprites and update the current sprite. It takes a sprite_list (the list of sprites to animate) and a speed (the speed of the animation). The method updates the current_sprite index, cycling through the sprite list at the specified speed. The image of the portal is then updated to the current sprite.

### Sprite Groups: 
After the Portal class definition, the code defines several sprite groups that will be used in the game:

* my_main_tile_group: A sprite group for the main tiles.
* my_platform_group: A sprite group for the platforms.
* my_player_group: A sprite group for the player.
* my_bullet_group: A sprite group for the bullets.
* my_zombie_group: A sprite group for the zombies.
* my_portal_group: A sprite group for the portals.
* my_ruby_group: A sprite group for the rubies.

Finally, the code defines a tile_map, which is a 2D list representing the layout of the game's tiles. Each number in the tile_map corresponds to a specific tile or object in the game world. The numbers are used to create the game's level layout.

After that, the code initiates the main game loop which initiates the game. 

## Credits
* The game was developed using the Pygame library.
* Sprite images were created by https://www.gameart2d.com/ and can be found in the images' folder.
* Sound effects were obtained from https://www.gameart2d.com/ and can be found in the sounds' folder.
The level design and gameplay mechanics were crafted by Savan Patel.

## Contributing
Contributions to Zombie Knight are welcome! If you encounter any issues or have suggestions for improvements, please create a new issue or submit a pull request. You can also contact me at sawanpatel2508@gmail.com. 