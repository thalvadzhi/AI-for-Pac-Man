# AI-for-Pac-Man
AI player for the game Pac-Man, based on the A* algorithm.

## Prerequisites
You need python 3.x to run the AI, and gcc to build the game.

## Installation
On Linux run `setup.sh` to generate the .so file containing the simulation of the ghost movement. 

Also run `cmake .` and after that `make` in order to build the Pac-Man executable.

All of these commands should be run from the root of the repo.

## Usage
First start the game by running `PacMan.elf`. The game will wait until the AI player connects with it, so until that happens an empty window will be shown. 

Run the AI with `python ./ai/main.py`. It is important to run the command from the root directory, otherwise the code will not start.

## Bonus info
Some quasirandom libraries are also included (e.g. library for the Sobol series etc.) they are used for the random simulation of the ghosts.

## Results
With our best efforts, Pac-Man wins around 70-80% of the time. Some room for improvement can be found in the simulation function and also in using Monte Carlo Tree Search instead of A*. 

