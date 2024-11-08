# rules.py

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
    directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
    king_directions = [(-i, -i) for i in range(1, 8)] + [(-i, i) for i in range(1, 8)] + [(i, -i) for i in range(1, 8)] + [(i, i) for i in range(1, 8)]

    mandatory_captures = []
    
    if specific_piece:
        pieces_to_check = [specific_piece]
    else:
        pieces_to_check = [(row, col) for row in range(8) for col in range(8) if board[row][col].lower() == player_color]

    for row, col in pieces_to_check:
        piece = board[row][col]
        if piece.lower() == player_color:
            if piece.isupper():
                for direction in king_directions:
                    step_row, step_col = direction
                    capture_possible = False
                    for distance in range(1, 8):
                        row_next = row + step_row * distance
                        col_next = col + step_col * distance

                        if not (0 <= row_next < 8 and 0 <= col_next < 8):
                            break

                        if board[row_next][col_next] == '.':
                            if capture_possible:
                                mandatory_captures.append(((row, col), (row_next, col_next)))
                                break
                        elif board[row_next][col_next].lower() != player_color.lower():
                            capture_possible = True
                        else:
                            break
            else:
                for direction in directions:
                    row_next = row + direction[0]
                    col_next = col + direction[1]

                    if not (0 <= row_next < 8 and 0 <= col_next < 8):
                        continue

                    mid_row = row + (row_next - row) // 2
                    mid_col = col + (col_next - col) // 2

                    if (board[row_next][col_next] == '.' and 
                        board[mid_row][mid_col].lower() != player_color.lower() and 
                        board[mid_row][mid_col] != '.'):
                        mandatory_captures.append(((row, col), (row_next, col_next)))

    return mandatory_captures