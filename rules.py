def is_valid_move(board, start_pos, end_pos, player_color):
    """
    Check if the move is valid according to checkers rules.
    Args:
        board (list): The current state of the board.
        start_pos (tuple): The starting position as (row, col).
        end_pos (tuple): The ending position as (row, col).
        player_color (str): The color of the current player ('w' for white, 'r' for red).
    Returns:
        bool: True if the move is valid, False otherwise.
    """
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    piece = board[start_row][start_col]

    print(f"[Valid Move] Start Pos: {start_pos}, End Pos: {end_pos}, Player Color: {player_color}, Piece: {piece}")  # Debug print
    
    if piece.lower() != player_color:
        print("[Valid Move] Piece color mismatch")
        return False
    
    if board[end_row][end_col] != '.':
        print("[Valid Move] End position not empty")
        return False

    row_diff = end_row - start_row
    col_diff = abs(end_col - start_col)

    if piece.isupper():  # King move
        if abs(row_diff) == abs(col_diff):
            # Ensure there are no pieces between the start and end positions
            step_row = row_diff // abs(row_diff)
            step_col = (end_col - start_col) // abs(end_col - start_col)
            mid_row, mid_col = start_row, start_col
            while (mid_row, mid_col) != (end_row, end_col):
                mid_row += step_row
                mid_col += step_col
                if board[mid_row][mid_col] != '.':
                    return False
            return True

    # Regular piece move
    if abs(row_diff) == 1 and col_diff == 1:
        if piece.lower() == 'w' and row_diff == -1:
            return True
        elif piece.lower() == 'r' and row_diff == 1:
            return True
    elif abs(row_diff) == 2 and col_diff == 2:
        mid_row = (start_row + end_row) // 2
        mid_col = (start_col + end_col) // 2
        mid_piece = board[mid_row][mid_col]
        if mid_piece.lower() != player_color and mid_piece != '.':
            return True

    print("[Valid Move] Move valid")
    return True

def is_capture_move(board, start_pos, end_pos, player_color):
    """
    Check if the move is a capturing move according to checkers rules.
    Args:
        board (list): The current state of the board.
        start_pos (tuple): The starting position as (row, col).
        end_pos (tuple): The ending position as (row, col).
        player_color (str): The color of the current player ('w' for white, 'r' for red).
    Returns:
        bool: True if the move is a capturing move, False otherwise.
    """
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    piece = board[start_row][start_col]

    if piece.lower() != player_color:
        return False
    
    if board[end_row][end_col] != '.':
        return False

    row_diff = end_row - start_row
    col_diff = abs(end_col - start_col)

    if piece.isupper():  # King move
        if abs(row_diff) == abs(col_diff) and abs(row_diff) > 1:
            step_row = row_diff // abs(row_diff)
            step_col = (end_col - start_col) // abs(end_col - start_col)
            mid_row, mid_col = start_row, start_col
            opponent_pieces = 0

            while (mid_row, mid_col) != (end_row, end_col):
                mid_row += step_row
                mid_col += step_col

                if board[mid_row][mid_col] != '.' and board[mid_row][mid_col].lower() != player_color:
                    opponent_pieces += 1
                elif board[mid_row][mid_col] != '.' and board[mid_row][mid_col].lower() == player_color:
                    return False

            return opponent_pieces == 1
    
    elif abs(row_diff) == 2 and col_diff == 2:
        mid_row = (start_row + end_row) // 2
        mid_col = (start_col + end_col) // 2
        mid_piece = board[mid_row][mid_col]
        if mid_piece.lower() != player_color and mid_piece != '.':
            return True
    
    return False

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

    mid_row = (start_row + end_row) // 2
    mid_col = (start_col + end_col) // 2

    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = '.'
    board[mid_row][mid_col] = '.'

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

def mandatory_capture(board, player_color):
    """
    Check for mandatory captures.
    Args:
        board (list): The current state of the board.
        player_color (str): The color of the current player ('w' for white, 'r' for red).
    Returns:
        list: A list of tuples indicating mandatory capture moves.
    """
    directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
    king_directions = [(-i, -i) for i in range(1, 8)] + [(-i, i) for i in range(1, 8)] + [(i, -i) for i in range(1, 8)] + [(i, i) for i in range(1, 8)]

    mandatory_captures = []

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece.lower() == player_color:
                if piece.isupper():
                    capture_check_directions = king_directions
                else:
                    capture_check_directions = directions

                for direction in capture_check_directions:
                    row_diff, col_diff = direction
                    row_next = row + row_diff
                    col_next = col + col_diff

                    if piece.isupper():
                        # Handle captures for flying kings over any distance
                        step_row = row_diff // abs(row_diff)
                        step_col = col_diff // abs(col_diff)
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
                        # Handle captures for regular pieces
                        row_capture = (row + row_next) // 2
                        col_capture = (col + col_next) // 2

                        if 0 <= row_next < 8 and 0 <= col_next < 8:
                            if board[row_next][col_next] == '.' and (board[row_capture][col_capture].lower() != player_color.lower() and board[row_capture][col_capture] != '.'):
                                mandatory_captures.append(((row, col), (row_next, col_next)))

    return mandatory_captures