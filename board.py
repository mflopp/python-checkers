# board.py

def initialize_board():
    """
    Function to initialize the checkers board with the standard setup.
    Returns:
        list: A 2D list representing the checkers board.
    """
    board = [['.' for _ in range(8)] for _ in range(8)]

    # Place black checkers (represented as 'r' for red) on the board
    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = 'r'

    # Place white checkers (represented as 'w' for white) on the board
    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col] = 'w'

    return board

def display_board(board, rotated=False):
    """
    Function to display the checkers board in the terminal.
    Args:
        board (list): A 2D list representing the checkers board.
        rotated (bool): A flag indicating if the board should be displayed rotated.
    """
    if rotated:
        horizontal_labels = "  h g f e d c b a"
        vertical_labels = range(1, 9)
        rows = range(7, -1, -1)
        cols = range(7, -1, -1)
    else:
        horizontal_labels = "  a b c d e f g h"
        vertical_labels = range(8, 0, -1)
        rows = range(8)
        cols = range(8)
    
    print(horizontal_labels)
    for row in rows:
        row_label = vertical_labels[7 - row] if rotated else vertical_labels[row]
        print(f"{row_label} ", end="")
        for col in cols:
            cell = board[row][col]
            if cell == 'r':
                print("\033[31m0\033[0m ", end="")  # Red checkers
            elif cell == 'w':
                print("\033[37m0\033[0m ", end="")  # White checkers
            elif cell == 'R':
                print("\033[31mX\033[0m ", end="")  # Red queen
            elif cell == 'W':
                print("\033[37mX\033[0m ", end="")  # White queen
            elif cell == '.':
                print("\033[37m.\033[0m ", end="")  # Grey dots for empty fields
        print(f"{row_label}")
    print(horizontal_labels)
