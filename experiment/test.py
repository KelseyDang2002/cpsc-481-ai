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
    return board[5][col_input] == 0

''' TODO '''
def get_next_open_row(board, col_input):
    for r in range(ROW_COUNT):
        if board[r][col_input] == 0:
            return r

''' Change orientatiom of board upside-down '''
def print_board(board):
    print(np.flip(board, 0))

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

    # Ask for Player 2 input
    else:
        col_input = int(input("Player 2 make your selection (0-6): "))

        if is_valid_location(board, col_input):
            row = get_next_open_row(board, col_input)
            place_piece(board, row, col_input, 2)

    print_board(board)

    turn += 1
    turn = turn % 2 # alternate turn to be equal to 0 or 1