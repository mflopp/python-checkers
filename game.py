# game.py

from board import initialize_board, display_board
from rules import apply_capture, promote_to_queen, mandatory_capture, non_capture_moves, is_game_over
from ui import get_player_names, display_welcome_message, display_move_prompt, display_invalid_move_message, display_capture_required_message, display_game_over_message

def get_move():
    """
    Function to get the move from the player.
    Returns:
        tuple: A tuple containing the starting position, ending position, and the sequence.
    """
    move = input("Enter your move (e.g., a3-b4-d6-f4): ").strip()
    
    # Split the input move string by '-' to get individual moves
    moves = move.split('-')
    
    # Check if the move sequence is valid
    # It must contain at least one complete move (start-end), hence minimum length should be 2
    # Also check that each move component is exactly 2 characters long and matches the format [a-h][1-8]
    if len(moves) < 2 or any(len(m) != 2 or m[0] not in "abcdefgh" or m[1] not in "12345678" for m in moves):
        print("Invalid move format. Please use the format [a-h][1-8]-[a-h][1-8]")
        return get_move()
    
    # Extract the starting and ending positions from the move list
    start_pos = moves[0]
    end_pos = moves[1]
    
    # Extract the sequence of moves after the starting and ending positions
    # If there are no additional moves, sequence will be an empty list
    sequence = moves[2:] if len(moves) > 2 else []
    
    # Return the start position, end position, and the sequence as a tuple
    return start_pos, end_pos, sequence

def convert_position(pos):
    """
    Convert board position from 'a3' format to (row, col) format.
    Args:
        pos (str): The board position in 'a3' format.
    Returns:
        tuple: A tuple containing row and column as integers.
    """
    # ord('a') - gets ASCII code of a letter. ASCII(a) - ASCII(b) is a distance between a and b
    col = ord(pos[0]) - ord('a')
    row = 8 - int(pos[1])  
    print(f"[Convert Position] Original: {pos}, Converted: {(row, col)}")  # Debug print
    return row, col

def make_move(board, start_pos, end_pos, player_color, sequence, rotated):
    """
    Make the move on the board if it is valid.
    Args:
        board (list): The current state of the board.
        start_pos (str): The starting position in 'a3' format.
        end_pos (str): The ending position in 'a3' format.
        player_color (str): The color of the current player ('w' for white, 'r' for red).
        sequence (list): The sequence of moves for a series of captures.
        rotated (bool): Flag indicating if the board is rotated.
    Returns:
        bool: True if the move was successful, False otherwise.
    """
    start_row, start_col = convert_position(start_pos)
    end_row, end_col = convert_position(end_pos)

    print(f"[Make Move] Start Pos: ({start_row}, {start_col}), End Pos: ({end_row}, {end_col}), Player Color: {player_color}, Piece: {board[start_row][start_col]}")  # Debug print
    capture_move_flag = False
    # get mandatory captures list
    possible_captures = mandatory_capture(board, player_color)
    print(f"[Make Move] Mandatory Captures: {possible_captures}")  # Debug print
    # if there are any mandatory captures
    if possible_captures:
        # check if the player's move is in the mandatory capture's list
        if ((start_row, start_col), (end_row, end_col)) not in possible_captures:
            display_capture_required_message()
            return False
        # setting captures move flag to True
        capture_move_flag = True
    # check if the player's move is a correct capture move
    if capture_move_flag:
        apply_capture(board, (start_row, start_col), (end_row, end_col))
        display_board(board, False)  # Debug print
        
        # check for mid-capture promotion to queen
        if (player_color == 'w' and end_row == 0) or (player_color == 'r' and end_row == 7):
            board[end_row][end_col] = board[end_row][end_col].upper()
            print(f"[Make Move] additional_capture after promoting to king: {board[end_row][end_col]}")  # Debug print
        
        # promote to queen during capture sequence (if applicable)
        promote_to_queen(board, (end_row, end_col))
        
        # check for additional possible captures
        # getting a new mandatory captures list
        additional_captures = mandatory_capture(board, player_color, specific_piece=(end_row, end_col))
        # if there are any mandatory captures
        if additional_captures:
            print(f"[Make Move] Additional Captures Available: {additional_captures}")  # Debug print
            # setting the starting point for the next capture
            next_capture_start = end_pos           
            # Check if sequence's first element matches additional_captures option
            if sequence:
                # trying to set the next position of the capturing peice according to the player's input
                next_capture_end = sequence[0]
                # checking if the next capture from user's input is possible and make a move if yes
                if ((end_row, end_col), convert_position(next_capture_end)) in additional_captures:
                    return make_move(board, next_capture_start, next_capture_end, player_color, sequence[1:], rotated)
                else:
                # setting sequence to empty because the player's input has incorrect moves
                    sequence = []  # Clear the sequence
            
            # Handle empty sequence or invalid sequence element
            # checking if there are more than one options to capture in additional_captures list
            if len(additional_captures) > 1:
                # displaying the game board with current position
                display_board(board, rotated)
                # asking palyer for the next move in his capture sequence
                _, next_capture_end, sequence = get_move()
            else:
                # if there is only one possible manadtory capture setting the next_capture_end
                next_capture_end = f"{chr(additional_captures[0][1][1] + ord('a'))}{8 - additional_captures[0][1][0]}"
            # making move according to all above to next_capture_end
            return make_move(board, next_capture_start, next_capture_end, player_color, sequence, rotated)

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
            start_pos, end_pos, sequence = get_move()
            # current player color flag
            player_color = 'w' if color == 'White' else 'r'
            print(f"[Play Game] Player: {current_player}, Color: {color}, Player Color: {player_color}")  # Debug print
            move_successful = make_move(board, start_pos, end_pos, player_color, sequence, rotated)
            if not move_successful:
                print("Please try again.")
        
        if is_game_over(board, player_color):
            display_game_over_message()
            break
                
        rotated = not rotated  # Toggle the rotation flag
        current_player_index = 1 - current_player_index  # Switch player turn

if __name__ == "__main__":
    play_game()
    