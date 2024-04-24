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
            
    # Check positively sloped diagonals (/)
    for c in range(COLUMN_COUNT - 3): # index 0 to index 4
        for r in range(ROW_COUNT - 3): # index 0 to index 3
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals (\)
    for c in range(COLUMN_COUNT - 3): # index 0 to index 4
        for r in range(3, ROW_COUNT): # index 3 through index 6
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

''' (AI) Function that evaulates windows of size 4 ''' 
def evaluate_window(window, piece):
    score = 0
    opponent_piece = PLAYER_PIECE
    
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE
    
    # Score
    if window.count(piece) == 4: # if window contains 4 pieces of same color = win
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1: # if window has 3 pieces of same color
        score += 20
    elif window.count(piece) == 2 and window.count(EMPTY) == 2: # if window has 2 pieces of same color
        score += 10
        
    # Opponent score
    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1: # opponent window has 3 pieces
        score -= 80
    elif window.count(opponent_piece) == 2 and window.count(EMPTY) == 2: # opponent window has 2 pieces
        score -= 20
        
    return score
            
''' (AI) Function to keep track of the score based on piece positions for the AI '''
def score_position(board, piece):
    score = 0
    # Center column score
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])] # COLUMN_COUNT // 2 = 4 = center column
    center_count = center_array.count(piece)
    score += center_count * 5
    
    # Horizontal score
    # AI will prioritize getting horizontal 4-in-a-rows
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])] # get all coloumn positions in a certain row r
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)
                
    # Vertical score
    # AI will also prioritize getting vertical 4-in-a-rows
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])] # get all row positions in a certain column c
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Positively sloped diagonal score (/)
    # AI prioritize 4-in-a-row in positive diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)] # start with r index i and c index i
            score += evaluate_window(window, piece)

    # Negatively sloped diagonal score (\)
    # AI prioritize 4-in-a-row in negative diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)] # start with r index 3 and c index i
            score += evaluate_window(window, piece)
                
    return score

''' (AI) Function that returns winning conditions or when there's no more valid locations '''
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

''' (AI) Function that performs Minimax algorithm '''
def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal: # when a terminal node is reached
            if winning_move(board, AI_PIECE):
                return (None, 100000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000)
            else: # game is over
                return (None, 0)
            
        else: # depth == 0
            return (None, score_position(board, AI_PIECE))
        
    if maximizingPlayer:
        value = -math.inf # V = -infinity
        column = random.choice(valid_locations)

        for col_input in valid_locations:
            row = get_next_open_row(board, col_input)
            board_copy = board.copy()
            place_piece(board_copy, row, col_input, AI_PIECE)

            new_score = minimax(board_copy, depth - 1, False)[1]

            if new_score > value:
                value = new_score
                column = col_input

        return column, value
        
    else: # Minimizing player
        value = math.inf # V = inifinity
        column = random.choice(valid_locations)

        for col_input in valid_locations:
            row = get_next_open_row(board, col_input)
            board_copy = board.copy()
            place_piece(board_copy, row, col_input, PLAYER_PIECE)

            new_score = minimax(board_copy, depth - 1, True)[1]

            if new_score < value:
                value = new_score
                column = col_input

        return column, value

''' (AI) Function that performs Minimax algorithm with Alpha-Beta Pruning '''
def minimax_alpha_beta(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    
    if depth == 0 or is_terminal:
        if is_terminal: # when a terminal node is reached
            if winning_move(board, AI_PIECE):
                return (None, 100000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000)
            else: # game is over
                return (None, 0)
            
        else: # depth == 0
            return (None, score_position(board, AI_PIECE))
        
    # Maximizing player
    if maximizingPlayer:
        value = -math.inf # V = -infinity
        column = random.choice(valid_locations)
        
        for col_input in valid_locations:
            row = get_next_open_row(board, col_input)
            board_copy = board.copy()
            place_piece(board_copy, row, col_input, AI_PIECE)

            new_score = minimax_alpha_beta(board_copy, depth - 1, alpha, beta, False)[1]
            
            if new_score > value: # get the highest scoring move
                value = new_score
                column = col_input
                
            alpha = max(alpha, value)
            
            if alpha >= beta:
                break
            
        return column, value
        
    else: # Minimizing player
        value = math.inf # V = inifinity
        column = random.choice(valid_locations)
        
        for col_input in valid_locations:
            row = get_next_open_row(board, col_input)
            board_copy = board.copy()
            place_piece(board_copy, row, col_input, PLAYER_PIECE)

            new_score = minimax_alpha_beta(board_copy, depth - 1, alpha, beta, True)[1]
            
            if new_score < value: # get the lowest scoring move
                value = new_score
                column = col_input
                
            beta = min(beta, value)
            
            if alpha >= beta:
                break
            
        return column, value

''' (AI) Function for AI to determine whether a location is valid '''
def get_valid_locations(board):
    valid_locations = [] # list of valid locations
    
    for col_input in range(COLUMN_COUNT):
        if is_valid_location(board, col_input): # if a location is valid then append to valid_locations list
            valid_locations.append(col_input)
    return valid_locations

''' (AI) Function for the AI to pick the best move '''
def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board) # get list of valid locations
    best_score = -100000
    best_col = random.choice(valid_locations) # randomly choose a location initially
    
    for col_input in valid_locations:
        row = get_next_open_row(board, col_input)
        temp_board = board.copy() # make a copy of board because we don't want to make modifications to original board
        place_piece(temp_board, row, col_input, piece) # place piece at the random location
        score = score_position(temp_board, piece) # score of location
        
        # check if score is the best score out of the valid locations
        if score > best_score:
            best_score = score
            best_col = col_input
            
    pygame.time.wait(500)

    return best_col

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
            print("\nGame exit.")
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
            
            # Player 1 turn
            if turn == PLAYER:
                posx = event.pos[0]
                col_input = int(math.floor(posx / SQUARE_SIZE)) # divide to get numbers 0-7

                if is_valid_location(board, col_input):
                    row = get_next_open_row(board, col_input)
                    place_piece(board, row, col_input, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        print("\nPLAYER 1 WINS!!!")
                        label = gamefont.render("PLAYER 1 WINS", PLAYER_PIECE, COLOR_RED) # create player win text
                        screen.blit(label, (40, 10))
                        game_over = True
                        
                    print_terminal_board(board)
                    draw_pygame_board(board)
                        
                    turn += 1
                    turn = turn % 2 # alternate turn to be equal to 0 or 1

                else: # invalid location
                    print("\nInvalid move, try again.")
                    turn -= 1

    # AI turn
    if turn == AI and not game_over:
        # col_input = random.randint(0, COLUMN_COUNT - 1) # randomly select column for computer piece
        # col_input = pick_best_move(board, AI_PIECE) # basic AI bot
        col_input, minimax_score = minimax(board, 4, True) # depth 5 starts to become slow
        # col_input, minimax_score = minimax_alpha_beta(board, 6, -math.inf, math.inf, True) # depth 7 starts to become slow

        if is_valid_location(board, col_input):
            row = get_next_open_row(board, col_input)
            place_piece(board, row, col_input, AI_PIECE)

            if winning_move(board, AI_PIECE):
                print("\nPLAYER 2 WINS!!!")
                label = gamefont.render("PLAYER 2 WINS", AI_PIECE, COLOR_YELLOW) # create player win text
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
        pygame.time.wait(1500)