# ai.py

import random
from rules import is_valid_move, is_capture_move, mandatory_capture, convert_position

def get_all_valid_moves(board, player_color):
    """
    Get all valid moves for the AI player.
    Args:
        board (list): The current state of the board.
        player_color (str): The color of the AI player ('w' for white, 'r' for red).
    Returns:
        list: A list of all valid moves as tuples ((start_row, start_col), (end_row, end_col)).
    """
    valid_moves = []
    for row in range(8):
        for col in range(8):
            if board[row][col].lower() == player_color:
                for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    end_row, end_col = row + dr, col + dc
                    if 0 <= end_row < 8 and 0 <= end_col < 8:
                        if is_valid_move(board, (row, col), (end_row, end_col), player_color):
                            valid_moves.append(((row, col), (end_row, end_col)))
                for dr, dc in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                    end_row, end_col = row + dr, col + dc
                    if 0 <= end_row < 8 and 0 <= end_col < 8:
                        if is_capture_move(board, (row, col), (end_row, end_col), player_color):
                            valid_moves.append(((row, col), (end_row, end_col)))
    return valid_moves

def get_ai_move(board, player_color):
    """
    Get a move from the AI player.
    Args:
        board (list): The current state of the board.
        player_color (str): The color of the AI player ('w' for white, 'r' for red).
    Returns:
        tuple: A tuple containing the starting and ending positions as (start_pos, end_pos).
    """
    valid_moves = get_all_valid_moves(board, player_color)
    if valid_moves:
        start_pos, end_pos = random.choice(valid_moves)
        return start_pos, end_pos
    return None
