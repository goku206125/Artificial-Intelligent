import numpy as np
import math
import time

# The point_modifier array assigns points to stones based on how many are in a row. Individually, each stone is
# worth point_modifier[1] points for every potential winning combination it is a part of. For an individual stone,
# the maximum number of points it can be worth is 20 * point_modifier[1]. Groups of two stones are worth
# point_modifier[2] for each winning combination. Five stones are worth double the winning threshold so that
# negative points, from the opposing player's pieces, don't inadvertantly reduce the winning player's score below
# the minimum threshold.

point_modifier = [0, 2, 5, 16, 50, 20000000]


# These functions look for possible win conditions in each of the four directions that the game can be won in. First,
# they determine if it is even possible to create a chain of five stones belonging to the same player. If it is, they
# find the furthest possible position from the starting point where a win is theoretically possible. Then, an imaginary
# chain of five stones travels in the other direction, one space at a time, until a point is reached where it is no
# longer possible for such a chain to exist. At each point, the number of stones actually part of the chain is counted
# and scored, based on the modifier. As a result, stones that are relatively unblocked can be counted many times, and are
# worth more than ones that are heavily blocked in. Since the win condition explicitly states that a chain must be exactly
# five stones long, any potential chains of 6 or longer are immediately disqualified from being scored. This procedure is
# performed for every stone on the board. As a result, when there are multiple stones in close proximity, the same win
# state (from the perspective of a different stone) may be counted multiple times, which artificially inflates the scores
# of stones belonging to larger and longer groups. This is considered a feature, since such a situation is beneficial in
# this game, where the goal is to build long chains of stones.

def analyze_vertical(board, origin_row, origin_col, player_stones, scoring_player, blocking_player):
    total_vertical_points = 0

    # Finds if a chain of five stones can be made and the earliest point it can start.
    max_possible_chain, row = get_start_point_vertical(board, origin_row, origin_col, player_stones, blocking_player)

    # If a chain of five cannot be made, the game can never be one with the current stone in this direction. So, zero
    # points are scored.
    if (max_possible_chain < 5):
        return total_vertical_points

    # Increment the imaginary chain, scoring points at each step.
    while (board[row][origin_col] != player_stones[blocking_player] and row <= (origin_row + 4)):
        total_vertical_points += get_points_vertical(board, row, origin_col, player_stones, scoring_player)

        if (row == 14):
            break
        else:
            row += 1

    return total_vertical_points

def get_start_point_vertical (board, origin_row, origin_col, player_stones, blocking_player):
    row = origin_row
    max_possible_chain = 1

    # Travel "backwards" until an opposing player's stone or the edge of the board is met. If neither of those
    # conditions are met, move until the last position where the current stone can still be part of the chain of
    # five.
    while (row != 0 and max_possible_chain < 5 and board[row - 1][origin_col] != player_stones[blocking_player]):
        row -= 1
        max_possible_chain += 1

    row = origin_row

    # If the chain is not filled, try to move forwards
    while (row != 14 and max_possible_chain < 5 and board[row + 1][origin_col] != player_stones[blocking_player]):
        row += 1
        max_possible_chain += 1

    return max_possible_chain, row

def get_points_vertical(board, row, col, player_stones, scoring_player):
    stone_count = 0

    # If the imaginary chain of five stones sees the current player's stone one tile in front or behind it, it is
    # not a possible win condition, as it would be a chain that is six stones long. So, it is not scored.
    if ((row - 4) != 0 and board[row - 5][col] == player_stones[scoring_player]):
        return 0
    elif (row != 14 and board[row + 1][col] == player_stones[scoring_player]):
        return 0

    # Count how many of the player's stones are actually in the chain and score based on the point modifier.
    for j in range(5):
        if (board[row - j][col] == player_stones[scoring_player]):
            stone_count += 1

    return point_modifier[stone_count]


# The same is repeated for the other three directions.
def analyze_horizontal(board, origin_row, origin_col, player_stones, scoring_player, blocking_player):
    total_horizontal_points = 0

    max_possible_chain, col = get_start_point_horizontal(board, origin_row, origin_col, player_stones, blocking_player)

    if (max_possible_chain < 5):
        return total_horizontal_points

    while (board[origin_row][col] != player_stones[blocking_player] and col <= (origin_col + 4)):
        total_horizontal_points += get_points_horizontal(board, origin_row, col, player_stones, scoring_player)

        if (col == 14):
            break
        else:
            col += 1

    return total_horizontal_points

def get_start_point_horizontal (board, origin_row, origin_col, player_stones, blocking_player):
    col = origin_col
    max_possible_chain = 1

    while (col != 0 and max_possible_chain < 5 and board[origin_row][col - 1] != player_stones[blocking_player]):
        col -= 1
        max_possible_chain += 1

    col = origin_col

    while (col != 14 and max_possible_chain < 5 and board[origin_row][col + 1] != player_stones[blocking_player]):
        col += 1
        max_possible_chain += 1

    return max_possible_chain, col

def get_points_horizontal (board, row, col, player_stones, scoring_player):
    stone_count = 0
    
    if ((col - 4) != 0 and board[row][col - 5] == player_stones[scoring_player]):
        return 0
    elif (col != 14 and board[row][col + 1] == player_stones[scoring_player]):
        return 0

    for j in range(5):
        if (board[row][col - j] == player_stones[scoring_player]):
            stone_count += 1

    return point_modifier[stone_count]



def analyze_diagonal1(board, origin_row, origin_col, player_stones, scoring_player, blocking_player):
    total_diagonal1_points = 0

    max_possible_chain, row, col = get_start_point_diagonal1(board, origin_row, origin_col, player_stones, blocking_player)

    if (max_possible_chain < 5):
        return total_diagonal1_points

    while (board[row][col] != player_stones[blocking_player] and row <= (origin_row + 4)):
        total_diagonal1_points += get_points_diagonal1(board, row, col, player_stones, scoring_player)

        if (row == 14 or col == 14):
            break
        else:
            row += 1
            col += 1

    return total_diagonal1_points

def get_start_point_diagonal1 (board, origin_row, origin_col, player_stones, blocking_player):
    row = origin_row
    col = origin_col
    max_possible_chain = 1

    while (row != 0 and col != 0 and max_possible_chain < 5 and board[row - 1][col - 1] != player_stones[blocking_player]):
        row -= 1
        col -= 1
        max_possible_chain += 1

    row = origin_row
    col = origin_col

    while (row != 14 and col != 14 and max_possible_chain < 5 and board[row + 1][col + 1] != player_stones[blocking_player]):
        row += 1
        col += 1
        max_possible_chain += 1

    return max_possible_chain, row, col

def get_points_diagonal1(board, row, col, player_stones, scoring_player):
    stone_count = 0
    
    if ((row - 4) != 0 and (col - 4) != 0 and board[row - 5][col - 5] == player_stones[scoring_player]):
        return 0
    elif (row != 14 and col != 14 and board[row + 1][col + 1] == player_stones[scoring_player]):
        return 0

    for j in range(5):
        if (board[row - j][col - j] == player_stones[scoring_player]):
            stone_count += 1

    return point_modifier[stone_count]



def analyze_diagonal2(board, origin_row, origin_col, player_stones, scoring_player, blocking_player):
    total_diagonal2_points = 0

    max_possible_chain, row, col = get_start_point_diagonal2(board, origin_row, origin_col, player_stones, blocking_player)

    if (max_possible_chain < 5):
        return total_diagonal2_points

    while (board[row][col] != player_stones[blocking_player] and col <= (origin_col + 4)):
        total_diagonal2_points += get_points_diagonal2(board, row, col, player_stones, scoring_player)

        if (row == 0 or col == 14):
            break
        else:
            row -= 1
            col += 1

    return total_diagonal2_points

def get_start_point_diagonal2 (board, origin_row, origin_col, player_stones, blocking_player):
    row = origin_row
    col = origin_col
    max_possible_chain = 1

    while (row != 14 and col != 0 and max_possible_chain < 5 and board[row + 1][col - 1] != player_stones[blocking_player]):
        row += 1
        col -= 1
        max_possible_chain += 1

    row = origin_row
    col = origin_col

    while (row != 0 and col != 14 and max_possible_chain < 5 and board[row - 1][col + 1] != player_stones[blocking_player]):
        row -= 1
        col += 1
        max_possible_chain += 1

    return max_possible_chain, row, col

def get_points_diagonal2(board, row, col, player_stones, scoring_player):
    stone_count = 0
    
    if ((row + 4) != 14 and (col - 4) != 0 and board[row + 5][col - 5] == player_stones[scoring_player]):
        return 0
    elif (row != 0 and col != 14 and board[row - 1][col + 1] == player_stones[scoring_player]):
        return 0

    for j in range(5):
        if (board[row + j][col - j] == player_stones[scoring_player]):
            stone_count += 1

    return point_modifier[stone_count]