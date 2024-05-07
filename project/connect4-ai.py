# Base code is from the Connect 4 game tutorial by Keith Galli on YouTube.
# The current code has been altered.

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
MM_DEPTH = 4 # depth 5 starts to become slow
AB_DEPTH = 4 # depth 7 starts to become slow

PLAYER = 0
AI = 1

EMPTY = 0
RED_PIECE = 1
YELLOW_PIECE = 2

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

def full_board(board):
    for row in board:
        for cell in row:
            if cell == 0:
                return False #if the cell is not empty,board is not full
    return True #if no empty cell, then the board is full

''' Function to get the next open row '''
def get_next_open_row(board, col_input):
    for r in range(ROW_COUNT):
        if board[r][col_input] == 0:
            return r

''' Function to change orientation of board upside-down '''
def print_terminal_board(board):
    print(end = "\n")
    print(np.flip(board, 0))

''' Function to print the terminal game menu '''
def print_terminal_menu():
    print("\n\t--- GAME MENU ---")
    print("\n1. Basic AI (R) vs Alpha-Beta (Y)")
    print("\n2. Minimax (R) vs Alpha-Beta (Y)")
    print("\n3. Alpha-Beta (R) vs Alpha-Beta (Y)")
    print("\n4. Player (R) vs Alpha-Beta (Y)")
    print("\n5. Player (R) vs Principle") #in progress and testing it out 

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

''' (AI) Function that evaluates windows of size 4 for red ''' 
def evaluate_window(window, piece):
    score = 0
    opponent_piece = YELLOW_PIECE
    
    if piece == YELLOW_PIECE:
        opponent_piece = RED_PIECE
    
    # Score
    if window.count(piece) == 4: # if window contains 4 pieces of same color = win
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1: # if window has 3 pieces of same color
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2: # if window has 2 pieces of same color
        score += 2
        
    # Opponent score
    if window.count(opponent_piece) == 3 and window.count(EMPTY) == 1: # opponent window has 3 pieces
        score -= 4
        
    return score
            
''' (AI) Function to keep track of the score based on piece positions for red '''
def score_position(board, piece):
    score = 0
    # Center column score
    # More pieces in center column = more possibilities for 4-in-a-rows = higher score
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])] # COLUMN_COUNT // 2 = 4 = center column
    center_count = center_array.count(piece)
    score += center_count * 3
    
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
                
    # print(f'Current score = {score}')
    return score

''' (AI) Function that evaluates windows of size 4 for yellow ''' 
def yellow_evaluate_window(window, piece):
    score = 0
    opponent_piece = RED_PIECE
    
    if piece == RED_PIECE:
        opponent_piece = YELLOW_PIECE
    
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

''' (AI) Function to keep track of the score based on piece positions for yellow '''
def yellow_score_position(board, piece):
    score = 0
    # Center column score
    # More pieces in center column = more possibilities for 4-in-a-rows = higher score
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])] # COLUMN_COUNT // 2 = 4 = center column
    center_count = center_array.count(piece)
    score += center_count * 5

    # Score based on indivudual board positions
    # Score = maximum possible 4-in-a-rows from this position
    # [3. 4. 5. 7. 5. 4. 3.]
    # [4. 6. 8. 10. 8. 6. 4.]
    # [5. 8. 11. 13. 11. 8. 5.]
    # [5. 8. 11. 13. 11. 8. 5.]
    # [4. 6. 8. 10. 8. 6. 4.]
    # [3. 4. 5. 7. 5. 4. 3.]
    # for r in range(ROW_COUNT):
    #     for c in range(COLUMN_COUNT):
    #         if board[2][3] or board[3][3]:
    #             score += 13
    #         elif board[2][2] or board[3][2] or board[2][4] or board[3][4]:
    #             score += 11
    #         elif board[1][3] or board[4][3]:
    #             score += 10
    #         elif board[2][1] or board[3][1] or board[1][2] or board[4][2] or board[1][4] or board[4][4] or board[2][5] or board[3][5]:
    #             score += 8
    #         elif board[0][3] or board[5][3]:
    #             score += 7
    #         elif board[1][1] or board[4][1] or board[1][5] or board[4][5]:
    #             score += 6
    #         elif board[2][0] or board[3][0] or board[0][2] or board[5][2] or board[0][4] or board[5][4] or board[2][6] or board[3][6]:
    #             score += 5
    #         elif board[1][0] or board[4][0] or board[0][1] or board[5][1] or board[0][5] or board[5][5] or board[1][6] or board[4][6]:
    #             score += 4
    #         else: # board[0][0] or board[5][0] or board[0][6] or board[5][6]
    #             score += 3
    
    # Horizontal score
    # AI will prioritize getting horizontal 4-in-a-rows
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])] # get all coloumn positions in a certain row r
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += yellow_evaluate_window(window, piece)
                
    # Vertical score
    # AI will also prioritize getting vertical 4-in-a-rows
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])] # get all row positions in a certain column c
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += yellow_evaluate_window(window, piece)

    # Positively sloped diagonal score (/)
    # AI prioritize 4-in-a-row in positive diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)] # start with r index i and c index i
            score += yellow_evaluate_window(window, piece)

    # Negatively sloped diagonal score (\)
    # AI prioritize 4-in-a-row in negative diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)] # start with r index 3 and c index i
            score += yellow_evaluate_window(window, piece)
                
    return score

''' (AI) Function that returns winning conditions or when there's no more valid locations '''
def is_terminal_node(board):
    return winning_move(board, RED_PIECE) or winning_move(board, YELLOW_PIECE) or len(get_valid_locations(board)) == 0

''' (AI) Function that performs Minimax algorithm '''
def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        minimax.counter += 1
        if is_terminal: # when a terminal node is reached
            if winning_move(board, RED_PIECE):
                return (None, 100000)
            elif winning_move(board, YELLOW_PIECE):
                return (None, -100000)
            else: # game is over
                return (None, 0)
            
        else: # depth == 0
            return (None, yellow_score_position(board, RED_PIECE))
        
    if maximizingPlayer:
        best_score = -math.inf # V = -infinity
        column = random.choice(valid_locations)

        for col_input in valid_locations:
            row = get_next_open_row(board, col_input)
            board_copy = board.copy()
            place_piece(board_copy, row, col_input, RED_PIECE)

            new_score = minimax(board_copy, depth - 1, False)[1]

            if new_score > best_score:
                best_score = new_score
                column = col_input

            # print(f'MAX explore:\tDepth: {depth}\tColumn: {column}\tBest Score: {best_score}')

        return column, best_score
        
    else: # Minimizing player
        best_score = math.inf # V = inifinity
        column = random.choice(valid_locations)

        for col_input in valid_locations:
            row = get_next_open_row(board, col_input)
            board_copy = board.copy()
            place_piece(board_copy, row, col_input, YELLOW_PIECE)

            new_score = minimax(board_copy, depth - 1, True)[1]

            if new_score < best_score:
                best_score = new_score
                column = col_input

            # print(f'MIN explore:\tDepth: {depth}\tColumn: {column}\tBest Score: {best_score}')

        return column, best_score
    
''' (AI) Function that performs Minimax algorithm with Alpha-Beta Pruning '''
def red_alpha_beta(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    
    if depth == 0 or is_terminal:
        red_alpha_beta.counter += 1
        if is_terminal: # when a terminal node is reached
            if winning_move(board, RED_PIECE):
                return (None, 100000)
            elif winning_move(board, YELLOW_PIECE):
                return (None, -100000)
            else: # game is over
                return (None, 0)
            
        else: # depth == 0
            return (None, yellow_score_position(board, RED_PIECE))
        
    # Maximizing player
    if maximizingPlayer:
        # best_score = -math.inf # V = -infinity
        best_score = alpha
        column = random.choice(valid_locations)
        
        for col_input in valid_locations:
            row = get_next_open_row(board, col_input)
            board_copy = board.copy()
            place_piece(board_copy, row, col_input, RED_PIECE)

            new_score = red_alpha_beta(board_copy, depth - 1, alpha, beta, False)[1]
            
            if new_score > best_score: # get the highest scoring move
                best_score = new_score
                column = col_input
                
            alpha = max(alpha, best_score)
            
            if alpha >= beta:
                break

            # print(f'MAX explore:\tDepth: {depth}\tColumn: {column}\tBest Score: {best_score}')
             
        return column, best_score
        
    else: # Minimizing player
        # best_score = math.inf # V = inifinity
        best_score = beta
        column = random.choice(valid_locations)
        
        for col_input in valid_locations:
            row = get_next_open_row(board, col_input)
            board_copy = board.copy()
            place_piece(board_copy, row, col_input, YELLOW_PIECE)

            new_score = red_alpha_beta(board_copy, depth - 1, alpha, beta, True)[1]
            
            if new_score < best_score: # get the lowest scoring move
                best_score = new_score
                column = col_input
                
            beta = min(beta, best_score)
            
            if alpha >= beta:
                break

            # print(f'MIN explore:\tDepth: {depth}\tColumn: {column}\tBest Score: {best_score}')
        
        return column, best_score

''' (AI) Function that performs Minimax algorithm with Alpha-Beta Pruning '''
def yellow_alpha_beta(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    
    if depth == 0 or is_terminal:
        yellow_alpha_beta.counter += 1
        if is_terminal: # when a terminal node is reached
            if winning_move(board, YELLOW_PIECE):
                return (None, 100000)
            elif winning_move(board, RED_PIECE):
                return (None, -100000)
            else: # game is over
                return (None, 0)
            
        else: # depth == 0
            return (None, yellow_score_position(board, YELLOW_PIECE))
        
    # Maximizing player
    if maximizingPlayer:
        # best_score = -math.inf # V = -infinity
        best_score = alpha
        column = random.choice(valid_locations)
        
        for col_input in valid_locations:
            row = get_next_open_row(board, col_input)
            board_copy = board.copy()
            place_piece(board_copy, row, col_input, YELLOW_PIECE)

            new_score = yellow_alpha_beta(board_copy, depth - 1, alpha, beta, False)[1]
            
            if new_score > best_score: # get the highest scoring move
                best_score = new_score
                column = col_input
                
            alpha = max(alpha, best_score)
            
            if alpha >= beta:
                break

            # print(f'MAX explore:\tDepth: {depth}\tColumn: {column}\tBest Score: {best_score}')
             
        return column, best_score
        
    else: # Minimizing player
        # best_score = math.inf # V = inifinity
        best_score = beta
        column = random.choice(valid_locations)
        
        for col_input in valid_locations:
            row = get_next_open_row(board, col_input)
            board_copy = board.copy()
            place_piece(board_copy, row, col_input, RED_PIECE)

            new_score = yellow_alpha_beta(board_copy, depth - 1, alpha, beta, True)[1]
            
            if new_score < best_score: # get the lowest scoring move
                best_score = new_score
                column = col_input
                
            beta = min(beta, best_score)
            
            if alpha >= beta:
                break

            # print(f'MIN explore:\tDepth: {depth}\tColumn: {column}\tBest Score: {best_score}')
        
        return column, best_score



''' (AI) Function for Alpha-Beta using Principal Variation Search '''
def yellow_AB_with_PVS(board, depth):
    yellow_alpha_beta.counter += 1
    best_move_sequence, best_score = principal_variation_search(board, depth, -math.inf, math.inf, YELLOW_PIECE)
    if best_move_sequence:
        return best_move_sequence[0]
    else:
        return None

''' (AI) Function that performs Principal Variation Search '''
def principal_variation_search(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        principal_variation_search.counter += 1
        if is_terminal: # when a terminal node is reached
            if winning_move(board, YELLOW_PIECE):
                return ([], 100000)
            elif winning_move(board, RED_PIECE):
                return ([], -100000)
            else: # game is over
                return ([], 0)
            
        else: # depth == 0
            return ([], score_position(board, YELLOW_PIECE))
    
    pvs_list = []
    # best_score = -math.inf
    # column = random.choice(valid_locations)

    for col_input in valid_locations:
        row = get_next_open_row(board, col_input)
        board_copy = board.copy()
        place_piece(board_copy, row, col_input, YELLOW_PIECE)

        if maximizingPlayer:
            score = -principal_variation_search(board, depth - 1, -beta, -alpha, False)[1]

        else:
            score = -principal_variation_search(board, depth - 1, -beta, -alpha, True)[1]

        undo_move(board, col_input, YELLOW_PIECE)

        if score >= beta:
            return ([], beta)
        
        if score > alpha:
            alpha = score
            pvs_list = [col_input] + pvs_list

    return pvs_list, alpha

''' (AI) Function to undo move in principal variation search '''
def undo_move(board, col_input, piece):
    # find lowest empty cell in column
    lowest_empty_row = find_lowest_empty_row(board, col_input)

    # remove last player's piece from the board
    board[lowest_empty_row][col_input] = 0

    # switch player
    piece = (piece - 1) % 2
    pass



''' (AI) Function to find lowest empty row '''
def find_lowest_empty_row(board, col_input):
    for row in range(ROW_COUNT - 1, -1, -1):
        if board[row][col_input] == 0:
            return row
    return -1

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
        score = yellow_score_position(temp_board, piece) # score of location
        
        # check if score is the best score out of the valid locations
        if score > best_score:
            best_score = score
            best_col = col_input
            
    pygame.time.wait(500)

    return best_col, best_score

''' Function to draw the pygame board GUI '''    
def draw_pygame_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # draws the board
            pygame.draw.rect(screen, COLOR_BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, COLOR_BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == RED_PIECE:
                # draws the red player pieces
                pygame.draw.circle(screen, COLOR_RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), window_height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

            elif board[r][c] == YELLOW_PIECE:
                # draws the yellow player pieces
                pygame.draw.circle(screen, COLOR_YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), window_height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)

    pygame.display.update()
    pygame.display.Info().current_w

''' Main '''
minimax.counter = 0
red_alpha_beta.counter = 0
yellow_alpha_beta.counter = 0
principal_variation_search.counter = 0

print_terminal_menu()
menu_input = int(input("\nSelect an option (1-4): "))

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

        # Basic AI turn
        if menu_input == 1:
            if turn == PLAYER:
                col_input, pbm_score = pick_best_move(board, RED_PIECE) # basic AI bot
                print(f'\nRED turn:\tColumn = {col_input}\tScore = {pbm_score}')

                while True:
                    if is_valid_location(board, col_input):
                        row = get_next_open_row(board, col_input)
                        place_piece(board, row, col_input, RED_PIECE)
                    else: # invalid location
                        print("\nInvalid move, try again.")
                        turn -= 1

                    if winning_move(board, RED_PIECE):
                        print("\nRED WINS!!!")
                        label = gamefont.render("RED WINS", RED_PIECE, COLOR_RED) # create player win text
                        screen.blit(label, (60, 10))
                        game_over = True
                    
                    if full_board(board):
                        print("TIE GAME!")
                        label = gamefont.render("TIE GAME!", True, COLOR_BLUE)
                        screen.blit(label, (60,10))
                        game_over = True
                        
                    print_terminal_board(board)
                    draw_pygame_board(board)
                        
                    turn += 1
                    turn = turn % 2 # alternate turn to be equal to 0 or 1

        # Minimax turn
        elif menu_input == 2:
            if turn == PLAYER:
                col_input, minimax_score = minimax(board, MM_DEPTH, True)
                print(f'\nRED turn:\tColumn = {col_input}\tScore = {minimax_score}')
                print(f'Minimax calls: {minimax.counter}')

                while True:
                    if is_valid_location(board, col_input):
                        row = get_next_open_row(board, col_input)
                        place_piece(board, row, col_input, RED_PIECE)
                    else: # invalid location
                        print("\nInvalid move, try again.")
                        turn -= 1

                    if winning_move(board, RED_PIECE):
                        print("\nRED WINS!!!")
                        label = gamefont.render("RED WINS", RED_PIECE, COLOR_RED) # create player win text
                        screen.blit(label, (60, 10))
                        game_over = True

                    if full_board(board):
                        print("TIE GAME!")
                        label = gamefont.render("TIE GAME!", True, COLOR_BLUE)
                        screen.blit(label, (60,10))
                        game_over = True
                        
                    print_terminal_board(board)
                    draw_pygame_board(board)
                        
                    turn += 1
                    turn = turn % 2 # alternate turn to be equal to 0 or 1
                    break

        # Alpha-Beta turn
        elif menu_input == 3:
            if turn == PLAYER:
                col_input, ab_score = red_alpha_beta(board, AB_DEPTH, -math.inf, math.inf, True)
                print(f'\nRED turn:\tColumn = {col_input}\tScore = {ab_score}')
                print(f'RED Alpha-Beta calls: {red_alpha_beta.counter}')
                
                while True:
                    if is_valid_location(board, col_input):
                        row = get_next_open_row(board, col_input)
                        place_piece(board, row, col_input, RED_PIECE)
                    else: # invalid location
                        print("\nInvalid move, try again.")
                        turn -= 1

                    if winning_move(board, RED_PIECE):
                        print("\nRED WINS!!!")
                        label = gamefont.render("RED WINS", RED_PIECE, COLOR_RED) # create player win text
                        screen.blit(label, (60, 10))
                        game_over = True
                        
                    if full_board(board):
                        print("TIE GAME!")
                        label = gamefont.render("TIE GAME!", True, COLOR_BLUE)
                        screen.blit(label, (60,10))
                        game_over = True
                        
                    print_terminal_board(board)
                    draw_pygame_board(board)
                        
                    turn += 1
                    turn = turn % 2 # alternate turn to be equal to 0 or 1
                    break

        # Player turn
        elif menu_input == 4:
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
                while True:
                    if turn == PLAYER:
                        posx = event.pos[0]
                        col_input = int(math.floor(posx / SQUARE_SIZE)) # divide to get numbers 0-7
                        print(f'\nRED turn:\tColumn = {col_input}')
                     
                        if is_valid_location(board, col_input):
                            row = get_next_open_row(board, col_input)
                            place_piece(board, row, col_input, RED_PIECE)
                        else:
                            print("\nInvalid move, try again.")
                            turn -= 1
                    
                    
                        if winning_move(board, RED_PIECE):
                            print("\nRED WINS!!!")
                            label = gamefont.render("RED WINS", RED_PIECE, COLOR_RED) # create player win text
                            screen.blit(label, (60, 10))
                            game_over = True
                        
                        if full_board(board):
                            print("TIE GAME!")
                            label = gamefont.render("TIE GAME!", True, COLOR_BLUE)
                            screen.blit(label, (60,10))
                            game_over = True
                        
                            
                        print_terminal_board(board)
                        draw_pygame_board(board)
                            
                        turn += 1
                        turn = turn % 2 # alternate turn to be equal to 0 or 1
                        break

                    #else: # invalid location
                        #print("\nInvalid move, try again.")
                        #turn -= 1
        
                        

    # Alpha-Beta turn
    if turn == AI and not game_over:
        # col_input, pvs_score = principal_variation_search(board, AB_DEPTH, -math.inf, math.inf, True)
        pvs_list, pvs_score = principal_variation_search(board, AB_DEPTH, -math.inf, math.inf, False)
        col_input, ab_score = yellow_alpha_beta(board, AB_DEPTH, -math.inf, math.inf, True)
        # col_input = yellow_AB_with_PVS(board, AB_DEPTH)

        print(f'\nPVS score:\t{pvs_score}\tPVS list: {pvs_list}')
        print(f'PVS calls:\t{principal_variation_search.counter}')
        print(f'\nYELLOW turn:\tColumn = {col_input}\tScore = {ab_score}')
        # print(f'\nYELLOW turn:\tColumn = {col_input}')
        print(f'YELLOW Alpha-Beta calls: {yellow_alpha_beta.counter}')

        if is_valid_location(board, col_input):
            row = get_next_open_row(board, col_input)
            place_piece(board, row, col_input, YELLOW_PIECE)

            if winning_move(board, YELLOW_PIECE):
                print("\nYELLOW WINS!!!")
                label = gamefont.render("YELLOW WINS", YELLOW_PIECE, COLOR_YELLOW) # create player win text
                screen.blit(label, (60, 10))
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