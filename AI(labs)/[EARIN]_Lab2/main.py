import numpy as np
import math
import time

from boardsimple import *
from minmax import *
from boardanalyze import *

# This program allows the user to play Gomoku against an AI. When the game ends, the program closes. The board state, as well
# as relevant information about the algorithms is printed after every move.

def gomoku():
    # Set equal to 0 to hide point values, 1 to show only the total point value of the board state, and 2 to show the point
    # values of all contributing stones as well as the total. 
    display_points = 2
    recursion_depth = 2     # how deep the min max algorithm goes
    optimization = True     # set to False to test slower version of alpha beta pruning algorithm     
    
    board = [['-' for _ in range(15)] for _ in range(15)]   # fills the board with dashes, representing empty spaces
    row_label = [(row + 1) for row in range(len(board))]    # prints a key on the right side of the board for ease of use
    col_label = [chr(ord('A') + col) for col in range(len(board[0]))]   # prints a key at the bottom, using letters to differentiate them from rows
    player_stones = ["X", "O"]      # symbols representing stones that will be used to mark each player's move
    current_player = 0
    turn_counter = 0

    print("Gomoku - X goes first\n\n")

    # The player can choose if they want to go first or second, essentially
    while True:
        human_player = input(f"Do you want to play as X or O? ")
        if (human_player.upper() == 'X' or human_player.upper() == 'O'):
            human_player = player_stones.index(human_player.upper())
            ai_player = 1 - human_player
            print()
            break
        else:
            print("Invalid input. Please enter either X or O.")
            continue

    
    print_board(board, row_label, col_label)
    
    # The game runs until either one player wins or there are no moves left
    while True:
        # If it is the player's turn, they can choose where they want to place their next piece. If it is the AI's turn, the program attempts to find
        # the best possible move using a min max algorithm with alpha beta pruning.
        if (current_player == human_player):
            try:
                inp_col, inp_row = input(f"{player_stones[current_player]}'s turn. Enter column (A-O) and row (1-15) separated by a space: ").split()
                col = col_label.index(inp_col.upper())
                row = row_label.index(int(inp_row))
                print()

            except ValueError:
                print("Invalid input. Please enter a letter and a number separated by a space.")
                continue

            if not valid_move(board, row, col):
                print("Invalid move. Please choose an empty cell on the board.")
                continue

            place_stone(board, row, col, player_stones[current_player])
        else:
            print(f"{player_stones[current_player]}'s turn.\n")

            start_time = time.time()

            # One of two versions of the algorithm will be run. They both employ alpha beta pruning and have the same depth. Their only difference is in the order
            # that their guesses are made.
            if (optimization == True):
                branch_count = ai_move_guess_optimized(board, player_stones, ai_player, human_player, -math.inf, math.inf, recursion_depth, recursion_depth, True, 0)
            else:
                branch_count = ai_move_guess_unoptimized(board, player_stones, ai_player, human_player, -math.inf, math.inf, recursion_depth, recursion_depth, True, 0)
            
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Shows how many branches have been pruned during each move
            total_branches = 1
            for j in range(recursion_depth):
                total_branches *= 225 - turn_counter - j
            total_branches += 1
            branches_pruned = total_branches - branch_count
            percent_pruned = 100 * branches_pruned / total_branches

            print(f"The algorithm took {elapsed_time} seconds to complete. Out of {total_branches} possible branches, {branches_pruned} were pruned ({percent_pruned} percent).\n")

        print_board(board, row_label, col_label)

        # Checks if there is a winner or a draw
        winner = check_win(board, player_stones, ai_player, human_player, display_points)
        if (winner != -1):
            print(f"{player_stones[winner]} wins!")
            break
        elif (turn_counter == 224):
            print("No more empty cells. The game is a draw!")
            break

        current_player = (current_player + 1) % 2
        turn_counter += 1

if __name__ == "__main__":
    gomoku()

