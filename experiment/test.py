# This code is not ours.
# This code is from the Connect 4 game tutorial by Keith Galli on YouTube.

import numpy as np
import pygame
import sys
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
WINDOW_LENGTH = 4
SQUARE_SIZE = 100 # Size of squares in window is 100 pixels
RADIUS = int(SQUARE_SIZE / 2 - 5) # radius for circles/player pieces

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

# define game colors
COLOR_BLUE = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)

''' Function to create the game board with 6 rows & 7 columns '''
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

''' Function to place piece in selected column '''
def place_piece(board, row, col_input, piece):
    board[row][col_input] = piece

''' Function to see if a location is valid when the top row is not filled '''
def is_valid_location(board, col_input):
    return board[ROW_COUNT - 1][col_input] == 0

''' Function to get the next open row '''
def get_next_open_row(board, col_input):
    for r in range(ROW_COUNT):
        if board[r][col_input] == 0:
            return r

''' Function to change orientation of board upside-down '''
def print_terminal_board(board):
    print(end = "\n")
    print(np.flip(board, 0))

''' Function that defines all 4-in-a-row winning combinations '''
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3): # Subtact 3 because 4-in-a-row cannot start at indeces 4-6
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
            
    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3): # Subtact 3 because 4-in-a-row cannot start at top 3 rows
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
            
    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3): # index 0 to index 4
        for r in range(ROW_COUNT - 3): # index 0 to index 3
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT):
        for r in range(3, ROW_COUNT): # index 3 through index 6
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
            
''' Function to keep track of the score based on piece positions for the AI '''
def score_position(board, piece):
    # Horizontal score
    score = 0
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])] # get all coloumn positions in a certain row r
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            
            if window.count(piece) == 4: # if window contains 4 pieces of same color = win
                score += 100
            elif window.count(piece) == 3 and window.count(EMPTY) == 1: # if window has 3 pieces of same color
                score += 10
                
    return score

''' Function to determine whether a location is valid '''
def get_valid_locations(board):
    valid_locations = []
    for col_input in range(COLUMN_COUNT):
        if is_valid_location(board, col_input):
            valid_locations.append(col_input)
        return valid_locations

''' Function for the AI to pick the best move '''
def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    for col_input in valid_locations:
        row = get_next_open_row(board, col_input)
        temp_board = board.copy()
        place_piece(temp_board, row, col_input, piece)
        # TODO

''' Function to draw the pygame board GUI '''    
def draw_pygame_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # draws the board
            pygame.draw.rect(screen, COLOR_BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, COLOR_BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                # draws the red player pieces
                pygame.draw.circle(screen, COLOR_RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), window_height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

            elif board[r][c] == AI_PIECE:
                # draws the yellow player pieces
                pygame.draw.circle(screen, COLOR_YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), window_height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    pygame.display.update()

''' Main '''
board = create_board()
print_terminal_board(board)
game_over = False
turn = random.randint(PLAYER, AI) # randomly selects who has first turn
pygame.init()
gamefont = pygame.font.SysFont("monospace", 75)

window_width = COLUMN_COUNT * SQUARE_SIZE
window_height = (ROW_COUNT + 1) * SQUARE_SIZE # +1 for the black top row
window_size = (window_width, window_height)
screen = pygame.display.set_mode(window_size)

draw_pygame_board(board)
pygame.display.update()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            # player piece follows mouse cursor
            pygame.draw.rect(screen, COLOR_BLACK, (0, 0, window_width, SQUARE_SIZE))
            posx = event.pos[0]

            if turn == PLAYER:
                # red player piece gets dropped
                pygame.draw.circle(screen, COLOR_RED, (posx, int(SQUARE_SIZE/2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Creates black top rectangle to cover player piece after a win
            pygame.draw.rect(screen, COLOR_BLACK, (0, 0, window_width, SQUARE_SIZE))
            
            # Player 1 input
            if turn == PLAYER:
                posx = event.pos[0]
                col_input = int(math.floor(posx / SQUARE_SIZE)) # divide to get numbers 0-7

                if is_valid_location(board, col_input):
                    row = get_next_open_row(board, col_input)
                    place_piece(board, row, col_input, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        print("\nPLAYER 1 WINS!!!")
                        label = gamefont.render("PLAYER 1 WINS", 1, COLOR_RED) # create player win text
                        screen.blit(label, (40, 10))
                        game_over = True
                        
                    print_terminal_board(board)
                    draw_pygame_board(board)
                        
                    turn += 1
                    turn = turn % 2 # alternate turn to be equal to 0 or 1

                else: # invalid location
                    print("\nInvalid move, try again.")
                    turn -= 1

    # Player 2 input
    if turn == AI and not game_over:
        col_input = random.randint(0, COLUMN_COUNT - 1) # randomly select column for computer piece

        if is_valid_location(board, col_input):
            pygame.time.wait(500)
            row = get_next_open_row(board, col_input)
            place_piece(board, row, col_input, AI_PIECE)

            if winning_move(board, AI_PIECE):
                print("\nPLAYER 2 WINS!!!")
                label = gamefont.render("PLAYER 2 WINS", 2, COLOR_YELLOW) # create player win text
                screen.blit(label, (40, 10))
                game_over = True

            print_terminal_board(board)
            draw_pygame_board(board)

            turn += 1
            turn = turn % 2 # alternate turn to be equal to 0 or 1
            
        else: # invalid location
            print("\nInvalid move, try again.")
            turn -= 1

    if game_over:
        pygame.time.wait(2000)