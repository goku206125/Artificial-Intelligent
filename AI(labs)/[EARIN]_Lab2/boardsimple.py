import numpy as np
import math
import time

def print_board(board, row_label, col_label):
    row_number = 0
    for row in board:
        print(" ".join(row), row_label[row_number])     # Adds spaces between dashes for better readability. Prints row label at the end.
        row_number += 1
    
    for col in col_label:
        print(col, end =" ")    # Prints column labels

    print("\n")

def valid_move(board, row, col):
    return board[row][col] == "-"

def place_stone(board, row, col, stone):
    board[row][col] = stone