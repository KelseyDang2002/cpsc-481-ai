# This code is not ours.
# This code is from the Connect 4 game tutorial by Keith Galli on YouTube.

import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

''' Create the game board with 6 rows & 7 columns '''
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

''' Place piece in selected column '''
def place_piece(board, row, col_input, piece):
    board[row][col_input] = piece

''' Location is valid if top row is not filled '''
def is_valid_location(board, col_input):
    return board[ROW_COUNT - 1][col_input] == 0

''' Get the next open row '''
def get_next_open_row(board, col_input):
    for r in range(ROW_COUNT):
        if board[r][col_input] == 0:
            return r

''' Change orientation of board upside-down '''
def print_board(board):
    print("\n")
    print(np.flip(board, 0))

''' All 4-in-a-row winning combinations '''
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

''' Main '''
board = create_board()
print_board(board)
game_over = False
turn = 0

while not game_over:
    # Ask for Player 1 input
    if turn == 0:
        col_input = int(input("Player 1 make your selection (0-6): "))

        if is_valid_location(board, col_input):
            row = get_next_open_row(board, col_input)
            place_piece(board, row, col_input, 1)

            if winning_move(board, 1):
                print("PLAYER 1 WINS!!!")
                game_over = True

    # Ask for Player 2 input
    else:
        col_input = int(input("Player 2 make your selection (0-6): "))

        if is_valid_location(board, col_input):
            row = get_next_open_row(board, col_input)
            place_piece(board, row, col_input, 2)

            if winning_move(board, 2):
                print("PLAYER 2 WINS!!!")
                game_over = True

    print_board(board)

    turn += 1
    turn = turn % 2 # alternate turn to be equal to 0 or 1