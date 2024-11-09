# rules.py

from ui import display_winner

def apply_capture(board, start_pos, end_pos):
    """
    Apply the capture move to the board.
    Args:
        board (list): The current state of the board.
        start_pos (tuple): The starting position as (row, col).
        end_pos (tuple): The ending position as (row, col).
    """
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    piece = board[start_row][start_col]
    board[end_row][end_col] = piece
    board[start_row][start_col] = '.'

    # Calculate the step increments for capturing pieces
    step_row = (end_row - start_row) // abs(end_row - start_row)
    step_col = (end_col - start_col) // abs(end_col - start_col)
    
    # Capture all opponent pieces in the path
    current_row, current_col = start_row + step_row, start_col + step_col
    while (current_row, current_col) != (end_row, end_col):
        if board[current_row][current_col].lower() != '.' and board[current_row][current_col].lower() != piece.lower():
            board[current_row][current_col] = '.'
        current_row += step_row
        current_col += step_col

def promote_to_queen(board, pos):
    """
    Promote a checker to a queen if it reaches the opposite side.
    Args:
        board (list): The current state of the board.
        pos (tuple): The position to check for promotion.
    """
    row, col = pos
    if board[row][col] == 'w' and row == 0:
        board[row][col] = 'W'  # White queen
    elif board[row][col] == 'r' and row == 7:
        board[row][col] = 'R'  # Red queen

def mandatory_capture(board, player_color, specific_piece=None):
    """
    Check for mandatory captures.
    Args:
        board (list): The current state of the board.
        player_color (str): The color of the current player ('w' for white, 'r' for red).
        specific_piece (tuple): A specific piece position to check for captures, if any.
    Returns:
        list: A list of tuples indicating mandatory capture moves.
    """
    # Directions for regular pieces (capture by jumping 2 squares in a direction)
    directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
    # Directions for king pieces (can capture in multiple steps in any diagonal direction)
    king_directions = [(-i, -i) for i in range(1, 8)] + [(-i, i) for i in range(1, 8)] + \
                      [(i, -i) for i in range(1, 8)] + [(i, i) for i in range(1, 8)]
    # variable to store mandatory capture moves
    mandatory_captures = []
    
    # Determine which pieces to check for mandatory captures
    if specific_piece:
        pieces_to_check = [specific_piece]
    else:
        pieces_to_check = [(row, col) for row in range(8) for col in range(8) if board[row][col].lower() == player_color]
    # Loop through each piece to check for possible captures
    for row, col in pieces_to_check:
        piece = board[row][col]
        if piece.lower() == player_color:
            # Check captures for king pieces
            if piece.isupper():
                for direction in king_directions:
                    step_row, step_col = direction
                    capture_possible = False
                    for distance in range(1, 8):
                        row_next = row + step_row * distance
                        col_next = col + step_col * distance
                        # Check if the position is within bounds
                        if not (0 <= row_next < 8 and 0 <= col_next < 8):
                            break
                        # Check if the next position is empty
                        if board[row_next][col_next] == '.':
                            if capture_possible:
                                mandatory_captures.append(((row, col), (row_next, col_next)))
                                continue  # Continue checking in the same direction for additional captures
                        # Check if the next position is an opponent's piece
                        elif board[row_next][col_next].lower() != player_color.lower() and board[row_next][col_next] != '.':
                            capture_possible = True
                        else:
                            break
            # Check captures for regular pieces
            else:
                for direction in directions:
                    row_next = row + direction[0]
                    col_next = col + direction[1]

                    if not (0 <= row_next < 8 and 0 <= col_next < 8):
                        continue
                    # Check if the position is within bounds
                    mid_row = row + (row_next - row) // 2
                    mid_col = col + (col_next - col) // 2
                    # Check if the next position is empty and there's an opponent's piece to capture
                    if (board[row_next][col_next] == '.' and 
                        board[mid_row][mid_col].lower() != player_color.lower() and 
                        board[mid_row][mid_col] != '.'):
                        mandatory_captures.append(((row, col), (row_next, col_next)))

    return mandatory_captures

def non_capture_moves(board, player_color):
    """
    Get all possible non-capturing moves for the player's pieces.
    Args:
        board (list): The current state of the board.
        player_color (str): The color of the current player ('w' for white, 'r' for red).
    Returns:
        list: A list of tuples indicating non-capturing moves.
    """
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    non_capture_moves_list = []

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece.lower() == player_color:
                # Check for regular non-capturing moves
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if board[new_row][new_col] == '.':
                            non_capture_moves_list.append(((row, col), (new_row, new_col)))

                if piece.isupper():  # Check for flying king non-capturing moves
                    for dr in range(-7, 8):
                        for dc in range(-7, 8):
                            if abs(dr) == abs(dc) and (dr != 0 or dc != 0):
                                new_row, new_col = row + dr, col + dc
                                if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] == '.':
                                    # Ensure there are no pieces blocking the path
                                    path_clear = True
                                    step_row = dr // abs(dr)
                                    step_col = dc // abs(dc)
                                    for step in range(1, abs(dr)):
                                        if board[row + step * step_row][col + step * step_col] != '.':
                                            path_clear = False
                                            break
                                    if path_clear:
                                        non_capture_moves_list.append(((row, col), (new_row, new_col)))

    return non_capture_moves_list

def is_game_over(board, player_color):
    """
    Check if the game is over.
    Args:
        board (list): The current state of the board.
        player_color (str): The color of the current player ('w' for white, 'r' for red).
    Returns:
        bool: True if the game is over, False otherwise.
    """
    opponent_color = 'r' if player_color == 'w' else 'w'

    opponent_pieces = sum(row.count(opponent_color) + row.count(opponent_color.upper()) for row in board)
    if opponent_pieces == 0 or not (mandatory_capture(board, opponent_color) or non_capture_moves(board, opponent_color)):
        display_winner('White' if opponent_color == 'r' else 'Black')
        return True

    return False