# Space Invader
This is a Python implementation of the classic game Space Invaders using the Pygame library.

# Getting Started
To play the game, you need to have Python installed on your computer. You can download and install Python from the official website: https://www.python.org/downloads/.

You also need to install the Pygame library. You can install it by running the following command:

pip install pygame

After installing Python and Pygame, you can clone the repository and run the game by executing the following command in the terminal:

python main.py

# How to Play

The goal of the game is to destroy all the aliens on the screen and prevent them from reaching the bottom. The player can move left and right using the arrow keys, and shoot bullets using the space bar.

The aliens move down the screen and change direction when they reach the edge. The game has multiple rounds, and each round has more aliens and they move faster.

The player has three lives, and the game ends when the player loses all lives. The score increases as the player destroys more aliens.

# Code Structure
The code is structured as follows:

main.py: The main file that contains the game loop and initializes the game objects.

This code is a basic implementation of the classic arcade game Space Invaders. The code uses Pygame library to create the game. The game is made up of a player-controlled character who tries to shoot down waves of aliens while avoiding their projectiles.

The code starts by importing the necessary libraries, Pygame and Random. Pygame is used for creating the game, while Random is used for generating random numbers. Pygame is then initialized to prepare the display surface.

The game window is set to a width of 1200 and a height of 700 pixels. A Pygame display surface object is created with the set_mode() function, which takes a tuple of the width and height as arguments. A caption is set for the game window using the set_caption() method.

The frame rate and clock objects are then set. The FPS variable sets the desired frame rate for the game, and the clock object is used to keep track of the game's timing.

The code defines a class, Game, which is used to manage and update the gameplay. The class takes several arguments: player, alien_group, player_bullet_group, and alien_bullet_group. These arguments represent the player object, the group of aliens, the player's bullets, and the aliens' bullets, respectively.

The Game class has several methods, including update(), draw(), shift_aliens(), check_collisions(), check_round_completion(), start_new_round(), and check_game_status().

The update() method updates the game by calling other methods like shift_aliens(), check_collisions(), and check_round_completion().

The draw() method is responsible for drawing the game's Heads Up Display (HUD) to the screen. It creates text surfaces for the score, round number, and remaining lives of the player, sets the color of the text to white, and blits them onto the display surface. Two lines are also drawn at the top and bottom of the screen using the draw.line() method.

The shift_aliens() method moves a wave of aliens down the screen and reverses their direction when they reach the edge. It also checks for any aliens that have breached the line of defense and reduces the player's remaining lives if necessary.

The check_collisions() method checks for collisions between the player's bullets and the aliens and between the aliens' bullets and the player. If a collision is detected, the appropriate sound is played, and the score or remaining lives are updated accordingly.

The check_round_completion() method checks if the current round has been completed by checking if there are any aliens left in the alien group. If there are no aliens left, the score is updated, and the round number is increased. A new round is then started using the start_new_round() method.

The start_new_round() method creates a new wave of aliens and pauses the game while waiting for the player to press the Enter key.

The check_game_status() method checks the game's status and displays the appropriate message to the player. If the player's lives are zero, the game is over, and the player is prompted to restart the game.

Overall, this code provides a basic implementation of the Space Invaders game, but it can be expanded and improved in various ways, such as adding more levels, power-ups, and sound effects.

# Credits
This game was developed by Savan Patel for educational purposes. The game is based on the classic game Space Invaders, which was created by Tomohiro Nishikado and released by Taito in 1978.
