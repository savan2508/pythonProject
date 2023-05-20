# Feed the Dragon
## Introduction
Feed the Dragon is a simple game developed using Python's Pygame library. In this game, the player controls a dragon and tries to catch coins while avoiding missing them. The goal is to collect as many coins as possible before running out of lives.

## Getting Started
Prerequisites
To run the game, you need to have Python 3 and Pygame installed on your system.

## Installing
* To install Pygame, run the following command in your terminal:

pip install pygame 

## Running the Game
* Please download feed_the_dragon.exe file and double click to run the file and start playing. 
* To run the game, navigate to the game's directory and execute the following command in your terminal:

python feed_the_dragon.py
## How to Play
The game is simple to play. Move the dragon up and down using the up and down arrow keys on your keyboard. The goal is to catch as many coins as possible while avoiding missing them. Every time you miss a coin, you lose a life. If you lose all your lives, the game is over. Your score increases by 1 every time you catch a coin.

## Code Structure
This is a Python program that utilizes the Pygame library to create a simple 2D game called "Feed the Dragon". In this game, the player controls a dragon and tries to catch coins that are falling from the top of the screen. The game has a score counter and a player lives counter that decreases when a coin is missed.

The program starts by importing the required libraries, which are the random library for generating random numbers, and the Pygame library for creating the game graphics and handling user inputs.

Then the program initializes the Pygame library and creates a display surface with a size of 1000 pixels by 400 pixels. It also sets the title of the window to "Feed the Dragon".

The game's values are set such as the player's starting life, velocity, and the coin's starting velocity and acceleration. There is also a buffer distance set for the coin to spawn and score and player lives that are initially set to 0 and 5, respectively.

Next, some colors and font for the text are set. The font is called 'AttackGraffiti.ttf' and the size is set to 32. The game's score text, title, lives text, game over text, and continue text are all rendered and assigned to their respective variables.

After that, the program loads the game assets such as music, sound effects, and images. The program sets the coin sound to be played when a coin is caught by the dragon and the miss sound when a coin is missed. The program also loads the background music, which is set to loop continuously.

The player and the coin images are loaded and assigned to their respective variables. The initial positions of these assets are also set. The player starts at the leftmost part of the screen, and the coin starts at the rightmost part of the screen with a random Y-position between 64 and the height of the screen minus 32.

The main game loop starts next, where the music is played continuously until the game is closed. The game loop listens for the quit event, and if the player closes the game window, the game stops. The program checks for user input and moves the dragon up and down accordingly.

The program then checks if the coin goes off-screen and misses the dragon. If that happens, the player loses a life, and the coin spawns at the rightmost part of the screen with a random Y-position. If the coin collides with the dragon, the score increases, and the coin spawns at the rightmost part of the screen with a random Y-position.

The program updates the score and lives text and checks if the player has run out of lives. If that happens, the game over text and the continue text are blitted on the screen. The game stops playing music, and the program waits for the player to press any key to continue. If the player wants to quit, the game stops.

Finally, the program fills the screen with black and blits the score, title, and lives text on the screen. It also draws a line below the text to separate it from the game assets. The program then blits the player and coin images on the screen and updates the display.

## Controls
* Up arrow key - Move the dragon up
* Down arrow key - Move the dragon down
# Credits
This game was created by Savan Patel for educational purpose. 
