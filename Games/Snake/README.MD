
# Snake Game
This is a basic implementation of the classic Snake game using the Pygame library in Python. The game involves moving a snake around the game screen, eating apples, and growing longer with each apple eaten. The game is over if the snake runs into the game screen's boundaries or its own body.

# Requirements
This program requires the following software and packages to run:

Python 3.x

Pygame library

# Getting Started
To run the program, you can simply run the snake_game.py file from the command line or an IDE.

# Game Interface
When you start the game, you will see a game screen with a snake and an apple. The snake's head is represented by a green rectangle, and its body consists of several other rectangles. The apple is represented by a red rectangle.

# Game Controls
* LEFT ARROW key: Move the snake left
* RIGHT ARROW key: Move the snake right
* UP ARROW key: Move the snake up
* DOWN ARROW key: Move the snake down
# Game Rules
* The game screen is a square, and the snake cannot move outside of its boundaries.
* The snake starts with a length of one.
* The snake will grow by one segment each time it eats an apple.
* If the snake runs into the game screen's boundaries or its own body, the game is over.
* Each time the snake eats an apple, the score increases by one.
# Game Logic
When the game starts, the program initializes the Pygame library and sets up a game screen. The game screen's size is 600 x 600 pixels, and the screen is filled with a white background.

The program then sets the game values, such as the size of the snake and the initial position of the snake's head. It also sets up the color scheme and fonts for the game.

Next, the program enters the main game loop, where it listens for user input, updates the game state, and renders the game screen.

In each iteration of the game loop, the program checks for user input. If the user presses an arrow key, the program updates the direction of the snake's movement accordingly.

The program then updates the snake's position by moving its head in the direction indicated by the user input. It also updates the position of the snake's body segments to follow the head.

If the snake's head collides with an apple, the program updates the score, plays a sound effect, and spawns a new apple at a random location on the game screen.

If the snake's head collides with the game screen's boundaries or its own body, the game is over. The program displays a "GAME OVER" message on the screen and waits for the user to press any key to restart the game.

# Conclusion
This implementation of the Snake game provides a fun and simple game to play using Python and Pygame. You can modify the program's values to make the game easier or more challenging, such as changing the size of the game screen or the speed of the snake's movement.

# Credits
This game was developed by Savan Patel for educational purposes. The original version of the Snake game was created in the mid-1970s by a programmer named Gremlin Industries for an arcade game called "Blockade". The game was later popularized by Nokia when it was included as a pre-installed game on their mobile phones in the late 1990s. Since then, there have been numerous versions and adaptations of the game developed by various companies and individuals.