import numpy as np
import math
import time

from directionalsweep import *

# These functions effectively act as the eyes of the AI, allowing it to see positions and groupings that are
# advantageous as well as those that are not. Since there are upwards 225! different possible board states, only searching for
# definitive win states is not feasable. Instead, it is assumed that every friendly piece has the potential to
# win the game, and the more potentials a player has, the more likely they are to win. Likewise, each opponent's
# piece has the potential to make the player lose. If there is no clear path to victory, the best possible move is
# likely the one that increases the player's potentials the most and decreases their opponent's potentials the
# most. This can be done by determining the total number of ways each player can win with each piece. Since larger groups
# of pieces clearly bring a player closer to victory but don't necessarily increase the number of ways that player can win,
# a modifier is used to encourage the AI to see larger and longer groups of pieces as a good investment.



# The modifier for achieving five pieces in a row is a very large number. This is so that the other modifiers can have a wide
# range of potential values without risking having certain nonwinning combinations with high values trigger the win condition
def check_win(board, player_stones, ai_player, human_player, print_points):
    total_board_points = analyze_board(board, player_stones, ai_player, human_player, print_points)

    if (total_board_points > 10000000):
        return ai_player
    elif (total_board_points < -10000000):
        return human_player
    else:
        return -1

# The board is searched for all stones. When one is found, its score is calculated and added to the total if it belongs to the AI
# and subtracted if it belongs to the player. Optionally, the point values of the potentials of each stone can be printed.
def analyze_board(board, player_stones, ai_player, human_player, print_points):
    total_board_points = 0

    for row in range(15):
        for col in range(15):
            if (board[row][col] == player_stones[ai_player]):
                total_stone_points = analyze_stone(board, row, col, player_stones, ai_player, human_player)
                total_board_points += total_stone_points

            elif (board[row][col] == player_stones[human_player]):
                total_stone_points = -analyze_stone(board, row, col, player_stones, human_player, ai_player)
                total_board_points += total_stone_points

            if (print_points == 2 and board[row][col] != "-"):
                print(f"{chr(col + 65)}  {row + 1}  pts: {total_stone_points}")

    if (print_points >= 1):
        print(f"Total pts: {total_board_points}\n")

    return total_board_points

# Once a stone is found, every possible winning combination that it can be a part of is determined.
def analyze_stone(board, row, col, player_stones, scoring_player, blocking_player):
    total_stone_points = 0

    total_stone_points += analyze_vertical(board, row, col, player_stones, scoring_player, blocking_player)
    total_stone_points += analyze_horizontal(board, row, col, player_stones, scoring_player, blocking_player)
    total_stone_points += analyze_diagonal1(board, row, col, player_stones, scoring_player, blocking_player)
    total_stone_points += analyze_diagonal2(board, row, col, player_stones, scoring_player, blocking_player)

    return total_stone_points