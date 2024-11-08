# game.py

from board import initialize_board, display_board
from rules import apply_capture, promote_to_queen, mandatory_capture
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
    capture_move_flag = False
    # check for mandatory captures
    possible_captures = mandatory_capture(board, player_color)
    print(f"[Make Move] Mandatory Captures: {possible_captures}")  # Debug print

    if possible_captures:
        if ((start_row, start_col), (end_row, end_col)) not in possible_captures:
            display_capture_required_message()
            return False
        capture_move_flag = True

    if capture_move_flag:
        apply_capture(board, (start_row, start_col), (end_row, end_col))
        display_board(board, rotated)  # Debug print
        
        # Promote mid-capture if crossing to the opponent's back row
        if (player_color == 'w' and end_row == 0) or (player_color == 'r' and end_row == 7):
            board[end_row][end_col] = board[end_row][end_col].upper()
            print(f"[Make Move] additional_capture after promoting to king: {board[end_row][end_col]}")  # Debug print
        
        # Promote to queen if applicable
        promote_to_queen(board, (end_row, end_col))
        
        # Check for additional captures only if the move was a capturing move
        additional_captures = mandatory_capture(board, player_color, specific_piece=(end_row, end_col))
        if additional_captures:
            print(f"[Make Move] Additional Captures Available: {additional_captures}")  # Debug print
            next_capture_start = end_pos
            next_capture_end = f"{chr(additional_captures[0][1][1] + ord('a'))}{8 - additional_captures[0][1][0]}"
            return make_move(board, next_capture_start, next_capture_end, player_color, rotated)

    else:
        non_capture_moves_list = non_capture_moves(board, player_color)
        if ((start_row, start_col), (end_row, end_col)) not in non_capture_moves_list:
            display_invalid_move_message()
            return False
        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = '.'
        
        # Promote to queen if applicable
        promote_to_queen(board, (end_row, end_col))

    return True

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
                
        rotated = not rotated  # Toggle the rotation flag
        current_player_index = 1 - current_player_index  # Switch player turn

if __name__ == "__main__":
    play_game()
    