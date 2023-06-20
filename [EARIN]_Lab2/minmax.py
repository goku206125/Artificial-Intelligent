import numpy as np
import math
import time

from boardanalyze import *


# These two algorithms attempt to bruteforce the best possible move by looking at every possible combination of moves that can be made until the end of the game.
# Unfortunately, as there are upwards of 225! possible game states, predicting more than two so moves ahead isn't very realistic. As such, the victory condition isn't
# the primary means of scoring. Instead, a score based on potential victories of players' stones is used and compared to choose the most ideal move. First, the
# AI places an imaginary stone at every possible position, one at a time. Then it does the same for the human player. In games with fewer possible states, this
# can usually be repeated several more times. Unless a victory condition is found immediately, the scores for each set of moves are calculated after the final
# move is made. Then, working backwards, the most optimal move for each player is made. With alpha beta pruning, assumptions about the best and worst case scenarios
# can be used to potentially eliminate branches before they are calculated, reducing computing time. Alpha beta pruning works best when the first moves calculated
# are the highest scoring ones. The unoptimized version of the algorithm goes through the board row by row, column by column starting at zero, which is the corner.
# The optimized version, on the other hand, starts in the middle of the board and travels outward in rings of increasing size. Since moves near the middle are more
# difficult to block, they score much higher than ones on the edges and in the corners. As such, the optimized version prunes significantly more branches than the
# unoptimized version.

def ai_move_guess_optimized(board, player_stones, ai_player, human_player, alpha, beta, depth, max_depth, maximizing_player, branch_count):
    total_board_points = analyze_board(board, player_stones, ai_player, human_player, 0)
    branch_count += 1
    branch_start_count = branch_count
    
    # If the maximum depth is reached or a victory condition is detected, the function stops making guesses.
    if (depth == 0 or abs(total_board_points) > 10000000):
        return total_board_points, branch_count

    # The function starts in the middle of the board
    row = 7
    col = 7
    ring_side_length = 0
    ring_move_count = 0

    if (maximizing_player):
        max_points = -math.inf
    else:
        min_points = math.inf

    while True:
        if (maximizing_player and board[row][col] == '-'):
            board[row][col] = player_stones[ai_player]      # temporarily place a stone
            total_board_points, branch_count = ai_move_guess_optimized(board, player_stones, ai_player, human_player, alpha, beta, depth - 1, max_depth, False, branch_count)
            board[row][col] = '-'   # remove the stone after the recursion is complete

            if (total_board_points > max_points):
                max_points = total_board_points     # AI player trying to maximize score
                best_row = row
                best_col = col
            
            alpha = max(alpha, total_board_points)
            if (beta <= alpha):     # prune condition for AI player
                break
        elif (board[row][col] == '-'):      # temporarily place a stone
            board[row][col] = player_stones[human_player]
            total_board_points, branch_count = ai_move_guess_optimized(board, player_stones, ai_player, human_player, alpha, beta, depth - 1, max_depth, True, branch_count)
            board[row][col] = '-'       # remove the stone after the recursion is complete

            if (total_board_points < min_points):
                min_points = total_board_points     # human player trying to minimize score
            
            beta = min(beta, total_board_points)
            if (beta <= alpha):     # prune condition for human player
                break
       
        # Loop conditions for traveling along board in rings of increasing size
        if (ring_move_count < ring_side_length):
            col += 1
            ring_move_count += 1
        elif (ring_move_count < (ring_side_length * 2)):
            row += 1
            ring_move_count += 1
        elif (ring_move_count < (ring_side_length * 3)):
            col -= 1
            ring_move_count += 1
        elif (ring_move_count < (ring_side_length * 4)):
            row -= 1
            ring_move_count += 1

        if (row == 0 and col == 0):
            break
        elif (ring_move_count == (ring_side_length * 4)):
            ring_side_length += 2
            ring_move_count = 0
            row -= 1
            col -= 1

    # Places a stone before returning for a final time.
    if (depth == max_depth):
        board[best_row][best_col] = player_stones[ai_player]
        print(f"{player_stones[ai_player]} places a piece on {chr(best_col + 65)} {best_row + 1}\n")
        return branch_count

    # Stops the recursion if there are no more moves to make
    if (branch_start_count == branch_count):
        return total_board_points, branch_count

    # Returns if depth < max_depth
    if (maximizing_player):
        return max_points, branch_count
    else:
        return min_points, branch_count


# This function is identical, except in the way that it travels along the board.
def ai_move_guess_unoptimized(board, player_stones, ai_player, human_player, alpha, beta, depth, max_depth, maximizing_player, branch_count):
    total_board_points = analyze_board(board, player_stones, ai_player, human_player, 0)
    branch_count += 1
    branch_start_count = branch_count
    
    if (depth == 0 or abs(total_board_points) > 10000000):
        return total_board_points, branch_count

    if (maximizing_player):
        max_points = -math.inf
    else:
        min_points = math.inf

    for row in range(15):
        for col in range(15):
            if (maximizing_player and board[row][col] == '-'):
                board[row][col] = player_stones[ai_player]
                total_board_points, branch_count = ai_move_guess_unoptimized(board, player_stones, ai_player, human_player, alpha, beta, depth - 1, max_depth, False, branch_count)
                board[row][col] = '-'

                if (total_board_points > max_points):
                    max_points = total_board_points
                    best_row = row
                    best_col = col
            
                alpha = max(alpha, total_board_points)
                if (beta <= alpha):
                    break
            elif (board[row][col] == '-'):
                board[row][col] = player_stones[human_player]
                total_board_points, branch_count = ai_move_guess_unoptimized(board, player_stones, ai_player, human_player, alpha, beta, depth - 1, max_depth, True, branch_count)
                board[row][col] = '-'

                if (total_board_points < min_points):
                    min_points = total_board_points
            
                beta = min(beta, total_board_points)
                if (beta <= alpha):
                    break
    
    if (depth == max_depth):
        board[best_row][best_col] = player_stones[ai_player]
        print(f"{player_stones[ai_player]} places a piece on {chr(best_col + 65)} {best_row + 1}\n")
        return branch_count

    if (branch_start_count == branch_count):
        return total_board_points, branch_count

    if (maximizing_player):
        return max_points, branch_count
    else:
        return min_points, branch_count