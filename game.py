# game.py

from board import initialize_board, display_board
from rules import apply_capture, promote_to_queen, mandatory_capture, non_capture_moves, is_game_over, finalize_captures
from ui import get_player_names, display_invalid_move_message, display_capture_required_message, display_game_over_message, display_winner
import random

def get_move(board, player_name, color, move_history, rotated):
    """
    Function to get the move from the player.
    Args:
        board, player_name, color, move_history, rotated - necessary evil to
            call display_board function for smooth vizualization in terminal
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
        display_board(board, player_name, color, move_history, rotated)
        print("\nInvalid move format. Please use the format [a-h][1-8]-[a-h][1-8]")
        return get_move(board, player_name, color, move_history, rotated)
    
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
    # print(f"[Convert Position] Original: {pos}, Converted: {(row, col)}")  # Debug print
    return row, col

def make_move(board, start_pos, end_pos, player_color, sequence, rotated, player_name, color, move_history, player_move):
    """
    Make the move on the board if it is valid.
    Args:
        board (list): The current state of the board.
        start_pos (str): The starting position in 'a3' format.
        end_pos (str): The ending position in 'a3' format.
        player_color (str): The color of the current player ('w' for white, 'r' for red).
        sequence (list): The sequence of moves for a series of captures.
        rotated (bool): Flag indicating if the board is rotated.
        player_name (str): The name of the current player.
        color (str): The color of the current player.
        move_history (list): stores the current move history
        player_move (list): A tmp storage of player's move sequence.
    Returns:
        bool: True if the move was successful, False otherwise.
    """
    start_row, start_col = convert_position(start_pos)
    end_row, end_col = convert_position(end_pos)

    # print(f"[Make Move] Start Pos: ({start_row}, {start_col}), End Pos: ({end_row}, {end_col}), Player Color: {player_color}, Piece: {board[start_row][start_col]}")  # Debug print
    capture_move_flag = False
    # get mandatory captures list
    possible_captures = mandatory_capture(board, player_color)
    # print(f"[Make Move] Mandatory Captures: {possible_captures}")  # Debug print
    # if there are any mandatory captures
    if possible_captures:
        # check if the player's move is in the mandatory capture's list
        if ((start_row, start_col), (end_row, end_col)) not in possible_captures:
            display_board(board, player_name, color, move_history, rotated)
            display_capture_required_message(possible_captures)
            return False
        # setting captures move flag to True
        capture_move_flag = True
        # add the current move to tmp player's move sequence
        if player_move:
            player_move[0] += "-" + end_pos
        else:
            player_move.append(start_pos + "-" + end_pos)
    # check if the player's move is a correct capture move
    if capture_move_flag:
        apply_capture(board, (start_row, start_col), (end_row, end_col), player_color)
        # display_board(board, player_name, color, False)  # Debug print
        
        # check for mid-capture promotion to queen
        if (player_color == 'w' and end_row == 0) or (player_color == 'r' and end_row == 7):
            board[end_row][end_col] = board[end_row][end_col].upper()
            # print(f"[Make Move] additional_capture after promoting to king: {board[end_row][end_col]}")  # Debug print
        
        # promote to queen during capture sequence (if applicable)
        promote_to_queen(board, (end_row, end_col))
        
        # check for additional possible captures
        # getting a new mandatory captures list
        additional_captures = mandatory_capture(board, player_color, specific_piece=(end_row, end_col))
        # if there are any mandatory captures
        if additional_captures:
            # print(f"[Make Move] Additional Captures Available: {additional_captures}")  # Debug print
            # setting the starting point for the next capture
            next_capture_start = end_pos           
            # Check if sequence's first element matches additional_captures option
            if sequence:
                # trying to set the next position of the capturing peice according to the player's input
                next_capture_end = sequence[0]
                # checking if the next capture from user's input is possible and make a move if yes
                if ((end_row, end_col), convert_position(next_capture_end)) in additional_captures:
                    
                    return make_move(board, next_capture_start, next_capture_end, player_color, sequence[1:], rotated, player_name, color,move_history, player_move)
                else:
                # setting sequence to empty because the player's input has incorrect moves
                    sequence = []  # Clear the sequence
            
            # Handle empty sequence or invalid sequence element
            # checking if there are more than one options to capture in additional_captures list
            if len(additional_captures) > 1:
                # displaying mandatory captures options and the game board with current position
                display_board(board, player_name, color, move_history, rotated)
                display_capture_required_message(additional_captures)
                # asking palyer for the next move in his capture sequence
                _, next_capture_end, sequence = get_move(board, player_name, color, move_history, rotated)
            else:
                # if there is only one possible manadtory capture setting the next_capture_end
                next_capture_end = f"{chr(additional_captures[0][1][1] + ord('a'))}{8 - additional_captures[0][1][0]}"
            # making move according to all above to next_capture_end
            return make_move(board, next_capture_start, next_capture_end, player_color, sequence, rotated, player_name, color,move_history, player_move)
    else:
        non_capture_moves_list = non_capture_moves(board, player_color)
        if ((start_row, start_col), (end_row, end_col)) not in non_capture_moves_list:
            display_board(board, player_name, color, move_history, rotated)
            display_invalid_move_message()
            return False
        board[end_row][end_col] = board[start_row][start_col]
        board[start_row][start_col] = '.'
        # adding player move to tmp list
        player_move.append(start_pos + "-" + end_pos)
        # Promote to queen if applicable
        promote_to_queen(board, (end_row, end_col))
    return True

def get_computer_move(board, player_color):
    possible_moves = mandatory_capture(board, player_color) or non_capture_moves(board, player_color)
    if possible_moves:
        return random.choice(possible_moves)
    return None

def play_game(choice, color_choice):
    """
    Function to manage the game play.
    """
    # print("\033c")
    # player1, player2 = get_player_names()
    if choice == "1":
        player1, player2 = get_player_names()
        players = [(player1, 'White'), (player2, 'Black')]
    else:
        player1 = input("\nEnter the name of player: ").strip()
        player2 = "Computer"
        if color_choice == "White":  
            players = [(player1, 'White'), (player2, 'Black')]
        else:
            players = [(player2, 'White'), (player1, 'Black')]   
    
    
    board = initialize_board()
    # Initialize move history for each player
    move_history = {"White": [], "Black": []}
    # players = [(player1, 'White'), (player2, 'Black')]
    # setting current player to whites and his board orientation
    current_player_index = 0
    # flag to rotate the board according to player's turn
    rotated = False

    while True:
        # initialize player's tmp move sequence
        player_move = []
        # getting current player's name and color
        player_name, color = players[current_player_index]
        display_board(board, player_name, color, move_history, rotated)
        print("\n")
        # flag to know if there was a successful move
        move_successful = False
        while not move_successful:
            # current player color flag
            player_color = 'w' if color == 'White' else 'r'
            if player_name == "Computer":
                start_pos, end_pos = None, None
                move = get_computer_move(board, 'r' if color == 'Black' else 'w')
                if move:
                    start_pos, end_pos = f"{chr(move[0][1] + ord('a'))}{8 - move[0][0]}", f"{chr(move[1][1] + ord('a'))}{8 - move[1][0]}"
                    move_successful = make_move(board, start_pos, end_pos, 'r' if color == 'Black' else 'w', [], rotated, player_name, color, move_history, player_move)
            else:
                start_pos, end_pos, sequence = get_move(board, player_name, color, move_history, rotated)
                # print(f"[Play Game] Player: {player_name}, Color: {color}, Player Color: {player_color}")  # Debug print
                move_successful = make_move(board, start_pos, end_pos, player_color, sequence, rotated, player_name, color, move_history, player_move)
        # adding full sequence of the current player's move to the move history
        move_history[color].append(player_move[0])
        # replace tagged for capture fields with dots
        finalize_captures(board)
        # check if the game is over after the current player's move
        if is_game_over(board, player_color):
            # getting the winner's name by color
            player_name = next(player[0] for player in players if player[1] == color)
            display_board(board, player_name, color, move_history, rotated)
            display_winner(player_name, color)
            display_game_over_message()
            break
                
        rotated = not rotated  # Toggle the rotation flag
        current_player_index = 1 - current_player_index  # Switch player turn

if __name__ == "__main__":
    play_game()
    