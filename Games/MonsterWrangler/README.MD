# Monster Wrangle
A simple game where the player must catch specific monsters to score points and progress through rounds.

# Getting Started
## Prerequisites
* Python 3
* Pygame

## Installation
1. Clone the repo
git clone https://github.com/savan2508/pythonProject/tree/master/Games/MonsterWrangler
2. Install Pygame
3. pip install pygame
4. Run the game
python main.py
# How to Play
* Use the arrow keys to move the player.
* The player must catch the monster that matches the color shown at the top of the screen.
* Each round has a time limit and the player must catch as many monsters as possible before time runs out.
* If the player catches the wrong monster or runs out of lives, the game is over.
* The player can use warps to move around the screen faster.
# Code Structure
This code is a Python program that uses the Pygame library to implement a game called "Monster Wrangle." The code defines a class called "Game," which controls the gameplay. The game displays a player and a group of monsters on a game screen. The objective of the game is to catch the monsters of a specific type displayed at the top of the screen by colliding with them while avoiding other types of monsters.

The code first imports the necessary libraries, including the "random" and "pygame" libraries. Then, it initializes the Pygame library by calling the "init()" function. It creates a display surface with a size of 1200 x 700 pixels and a caption "Monster Wrangle" by calling the "set_mode()" and "set_caption()" functions, respectively. It also sets the frame per second (FPS) to 60 and creates a clock object to control the speed of the game.

The "Game" class is defined with an "init" function that initializes the game object with the score, round number, round time, and frame count set to 0. It also initializes the player and monster_group, loads sound and music files, sets images for the monsters, and randomly selects a target monster from the available types.

The "update()" function updates the game by incrementing the frame count and round time. It also checks for collisions between the player and the monsters by calling the "check_collision()" function.

The "draw()" function draws the HUD and other display elements on the game screen. It sets the colors and fonts of the text and blits them onto the surface. It also draws rectangles around the target monster and the game screen.

The "check_collision()" function checks for collisions between the player and the monsters. If a collision occurs, it checks if the collided monster is of the target type. If so, it increments the score, removes the monster, and chooses a new target. If the collided monster is not of the target type, it decrements the player's lives, resets the player, and checks if the game is over.

Overall, the code defines a functional game with basic features, such as collision detection, scoring, and player lives.
# Credits
This game was created by Savan Patel for educational purpose. 
