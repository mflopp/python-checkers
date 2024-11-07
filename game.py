# game.py

from board import initialize_board, display_board
from rules import is_valid_move, is_capture_move, apply_capture, promote_to_queen, mandatory_capture
from ui import get_player_names, display_welcome_message, display_move_prompt, display_invalid_move_message, display_capture_required_message, display_winner, display_draw_message, display_game_over_message

def get_move():
    """
    Function to get the move from the player.
    Returns:
        tuple: A tuple containing the starting position and ending position.
    """
    move = input("Enter your move (e.g., a3-b4): ").strip()
    if len(move) != 5 or move[2] != '-':
        print("Invalid move format. Please use the format a3-b4.")
        return get_move()
    start_pos, end_pos = move.split('-')
    return start_pos, end_pos

def convert_position(pos, rotated):
    """
    Convert board position from 'a3' format to (row, col) format.
    Args:
        pos (str): The board position in 'a3' format.
        rotated (bool): A flag indicating if the board is rotated.
    Returns:
        tuple: A tuple containing row and column as integers.
    """
    col = ord(pos[0]) - ord('a')
    row = 8 - int(pos[1])
    if rotated:
        col = 7 - col
        row = 7 - row
    print(f"[Convert Position] Original: {pos}, Converted: {(row, col)}, Rotated: {rotated}")  # Debug print
    return row, col

def make_move(board, start_pos, end_pos, player_color, rotated):
    """
    Make the move on the board if it is valid.
    Args:
        board (list): The current state of the board.
        start_pos (str): The starting position in 'a3' format.
        end_pos (str): The ending position in 'a3' format.
        player_color (str): The color of the current player ('w' for white, 'r' for red).
        rotated (bool): A flag indicating if the board is rotated.
    Returns:
        bool: True if the move was successful, False otherwise.
    """
    start_row, start_col = convert_position(start_pos, rotated)
    end_row, end_col = convert_position(end_pos, rotated)

    print(f"[Make Move] Start Pos: ({start_row}, {start_col}), End Pos: ({end_row}, {end_col}), Player Color: {player_color}, Piece: {board[start_row][start_col]}")  # Debug print
    capture_move_flag = is_capture_move(board, (start_row, start_col), (end_row, end_col), player_color)
    # Check for mandatory captures
    possible_captures = mandatory_capture(board, player_color)
    print(f"[Make Move] Mandatory Captures: {possible_captures}")  # Debug print
    if possible_captures and not capture_move_flag:
        display_capture_required_message()
        return False

    if capture_move_flag:
        apply_capture(board, (start_row, start_col), (end_row, end_col))
        
        # Promote mid-capture if crossing to the opponent's back row
        if (player_color == 'w' and end_row == 0) or (player_color == 'r' and end_row == 7):
            board[end_row][end_col] = board[end_row][end_col].upper()
            # Check for additional captures as a king
            print(f"[Make Move] additional_capture after promoting to king: {board[end_row][end_col]}") # debug print)
            additional_captures(board, (end_row, end_col), player_color, rotated)
    else:
        if not is_valid_move(board, (start_row, start_col), (end_row, end_col), player_color):
            display_invalid_move_message()
            return False
        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = '.'

    promote_to_queen(board, (end_row, end_col))
    
    # Check for additional captures only if the move was a capturing move
    if capture_move_flag:
        additional_captures(board, (end_row, end_col), player_color, rotated)
    
    return True

def additional_captures(board, pos, player_color, rotated):
    """
    Check for additional captures and prompt the player to continue if possible.
    Args:
        board (list): The current state of the board.
        pos (tuple): The position of the piece after the last capture.
        player_color (str): The color of the current player ('w' for white, 'r' for red).
        rotated (bool): A flag indicating if the board is rotated.
    """
    row, col = pos
    directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
    king_directions = [(-i, -i) for i in range(1, 8)] + [(-i, i) for i in range(1, 8)] + [(i, -i) for i in range(1, 8)] + [(i, i) for i in range(1, 8)]

    piece = board[row][col]
    is_king = piece.isupper()

    while True:
        possible_captures = []
        if is_king:
            capture_check_directions = king_directions
        else:
            capture_check_directions = directions

        for direction in capture_check_directions:
            row_diff, col_diff = direction
            row_next = row + row_diff
            col_next = col + col_diff

            if is_king:
                # Check for any distance in diagonal direction for kings
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
                            possible_captures.append((row_next, col_next))
                    elif board[row_next][col_next].lower() != player_color.lower():
                        capture_possible = True
                    else:
                        break
            else:
                # Regular piece capture logic
                row_capture = (row + row_next) // 2
                col_capture = (col + col_next) // 2

                if 0 <= row_next < 8 and 0 <= col_next < 8:
                    if board[row_next][col_next] == '.' and (board[row_capture][col_capture].lower() != player_color.lower() and board[row_capture][col_capture] != '.'):
                        possible_captures.append((row_next, col_next))

        if not possible_captures:
            break  # No more captures available

        for capture_pos in possible_captures:
            print(f"Additional capture available from {pos} to {capture_pos}")

        # Assume the first available capture is chosen
        next_pos = possible_captures[0]

        # Convert the positions back to string format
        start_pos_str = f"{chr(col + ord('a'))}{8 - row}"
        end_pos_str = f"{chr(next_pos[1] + ord('a'))}{8 - next_pos[0]}"
        
        move_successful = make_move(board, start_pos_str, end_pos_str, player_color, rotated)
        if move_successful:
            row, col = next_pos
        else:
            print("Invalid move during additional captures. Please follow the rules of Checkers and try again.")
            break

def has_valid_moves(board, player_color):
    """
    Check if the player has any valid moves left.
    Args:
        board (list): The current state of the board.
        player_color (str): The color of the current player ('w' for white, 'r' for red).
    Returns:
        bool: True if the player has valid moves, False otherwise.
    """
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    capture_directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)]
    king_directions = [(-i, -i) for i in range(1, 8)] + [(-i, i) for i in range(1, 8)] + [(i, -i) for i in range(1, 8)] + [(i, i) for i in range(1, 8)]

    for row in range(8):
        for col in range(8):
            piece = board[row][col].lower()
            if piece == player_color:
                for dr, dc in directions:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if is_valid_move(board, (row, col), (new_row, new_col), player_color):
                            return True
                for dr, dc in capture_directions:
                    new_row, new_col = row + dr, col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        if is_capture_move(board, (row, col), (new_row, new_col), player_color):
                            return True
            elif piece == player_color and board[row][col].isupper():  # Check for queens/kings
                for dr in range(-7, 8):
                    for dc in range(-7, 8):
                        if abs(dr) == abs(dc):
                            new_row, new_col = row + dr, col + dc
                            if 0 <= new_row < 8 and 0 <= new_col < 8 and (dr != 0 or dc != 0):
                                if is_valid_move(board, (row, col), (new_row, new_col), player_color):
                                    return True
                                if is_capture_move(board, (row, col), (new_row, new_col), player_color):
                                    return True
    return False

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
    if opponent_pieces == 0 or not has_valid_moves(board, opponent_color):
        display_winner('White' if opponent_color == 'r' else 'Black')
        return True

    return False

def play_game():
    """
    Function to manage the game play.
    """
    display_welcome_message()
    player1, player2 = get_player_names()
    board = initialize_board()
    players = [(player1, 'White'), (player2, 'Black')]
    # setting current player to whites and his board orientation
    current_player_index = 0
    rotated = False

    while True:
        current_player, color = players[current_player_index]
        display_move_prompt(current_player)
        display_board(board, rotated)
        # flag to know if there was a successful move
        move_successful = False
        while not move_successful:
            start_pos, end_pos = get_move()
            # current player color flag
            player_color = 'w' if color == 'White' else 'r'
            print(f"[Play Game] Player: {current_player}, Color: {color}, Player Color: {player_color}")  # Debug print
            move_successful = make_move(board, start_pos, end_pos, player_color, False)
            if not move_successful:
                print("Please try again.")
        
        if is_game_over(board, player_color):
            display_game_over_message()
            break
        
        # Only check for additional captures if the move was a capturing move
        if is_capture_move(board, convert_position(start_pos, rotated), convert_position(end_pos, rotated), player_color):
            while True:
                display_move_prompt(current_player)
                display_board(board, rotated)
                move_successful = False
                while not move_successful:
                    start_pos, end_pos = get_move()
                    move_successful = make_move(board, start_pos, end_pos, player_color, rotated)
                    if move_successful:
                        additional_captures(board, convert_position(end_pos, rotated), player_color, rotated)
                    else:
                        print("Please try again.")
                if not mandatory_capture(board, player_color):
                    break
        
        rotated = not rotated  # Toggle the rotation flag
        current_player_index = 1 - current_player_index  # Switch player turn

if __name__ == "__main__":
    play_game()
    