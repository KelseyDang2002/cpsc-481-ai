# CPSC 481 Artificial Intelligence Project

## Group Members:
1. Name: Kelsey Dang&emsp;&emsp;Email: kdangdo2002@csu.fullerton.edu
2. Name: Jayson Doty&emsp;&emsp;Email: jayson.doty@csu.fullerton.edu
3. Name: Steven Liu &emsp;&emsp;Email: sttvn@csu.fullerton.edu
4. Name: Kelly Kuoch&emsp;&emsp;Email: ykuoc00001@csu.fullerton.edu

## Layout of Code

## How to Execute and Interact with Program

### Setup

1. Install the following Python libraries:
    - import numpy as np
    - import pygame
    - import sys
    - import math
    - import random
2. Navigate to the project folder

### Program Execution

1. To execute the program, run the following command in the terminal:

```console
python connect4-ai.py
```

2. Select one of the four options by typing the corresponding number (1-4):

```console
        --- GAME MENU ---

1. Basic AI (R) vs Alpha-Beta (Y)

2. Minimax (R) vs Alpha-Beta (Y)

3. Alpha-Beta (R) vs Alpha-Beta (Y)

4. Player (R) vs Alpha-Beta (Y)

Select an option (1-4): 
```

3. The Pygame window should open up. If the window is running in the background, simply click on the Pygame window from your computer desktop taskbar to bring it forward.

## What Does Each File/Folder Do

### experiment folder

The experiment folder contains any files that can be used for experimenting or testing the code.
- function.py
    - Ignore this file, it does not contribute to the final code
- test.py
    - File to test and experiment with the Connect Four game from the YouTube tutorial by Keith Galli
- test2.py
    - File to test and experiment with the Connect Four code from codeNewb204's Github repository

### project folder

The project folder contains the source code of our Connect Four AI.
- connect4.py
    - Starting code of the Connect Four game followed by a YouTube tutorial by Keith Galli
- connect4-terminal.py
    - Starting code of terminal Connect Four from codeNewb204's Github repository, ignore this file since it does not contribute to the final code
- connect4-ai.py
    - The final source code that we worked on, contains minimax alpha-beta implementation from the YouTube tutorial by Keith Galli

## References
1. YouTube Connect 4 /w Minimax Tutorial: https://www.youtube.com/watch?v=MMLtza3CZFM&t=2810s 
2. YouTube Connect Four with Minimax Alpha-Beta Pruning Code Github Repository (Starting Code): https://github.com/KeithGalli/Connect4-Python/blob/master/connect4_with_ai.py 
3. Existing Terminal Connect Four Code Github Repository: https://github.com/codeNewb204/Terminal-Game/blob/main/Connect4.py 