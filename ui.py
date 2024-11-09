# ui.py

def get_player_names():
    """
    Function to get the names of the players.
    Returns:
        tuple: A tuple containing the names of player 1 and player 2.
    """
    player1 = input("Enter the name of player 1 (White): ").strip()
    player2 = input("Enter the name of player 2 (Black): ").strip()
    return player1, player2

def display_welcome_message():
    """
    Function to display a welcome message at the start of the game.
    """
    print("Welcome to Checkers!")
    print("Players will take turns to move their pieces.")
    print("White moves first.")
    print("Enter your move in the format 'a3-b4'.")
    print("Let's begin!\n")
def display_move_prompt(player):
    """
    Function to display the move prompt for the player.
    Args:
        player (str): The name of the current player.
    """
    print(f"{player}, it's your turn.")

def display_invalid_move_message():
    """
    Function to display a message for an invalid move.
    """
    print("Invalid move. Please follow the rules of Checkers and try again.")

def display_capture_required_message(possible_captures):
    """
    Function to display a message when a capture is required, including all mandatory capture options.
    Args:
        possible_captures (list): A list of tuples indicating mandatory capture moves.
    """
    # Initialize a list to hold the human-friendly capture moves
    capture_moves = []
    
    # Convert the capture moves to human-friendly format
    for start, end in possible_captures:
        start_pos = f"{chr(start[1] + ord('a'))}{8 - start[0]}"
        end_pos = f"{chr(end[1] + ord('a'))}{8 - end[0]}"
        capture_moves.append(f"{start_pos}-{end_pos}")
    
    # Display the message with the list of capture moves
    print("You have a mandatory capture. Please make a capturing move.")
    print("Mandatory capture options: " + ", ".join(capture_moves))

# Example usage
# possible_captures = [((2, 0), (0, 2)), ((4, 4), (2, 6))]
# display_capture_required_message(possible_captures)

def display_winner(player_name, player_color):
    """
    Function to display the winner message.
    Args:
        player_name (str): The name of the winning player.
        player_color (str): The color of the winning player.
    """
    print(f"\n{player_name} ({player_color}) is the winner. Congratulations!")

# def display_draw_message():
#     """
#     Function to display a message when the game is a draw.
#     """
#     print("The game is a draw. Well played, both players!")
def display_game_over_message():
    """
    Function to display a game over message.
    """
    print("Game over. Thank you for playing Checkers!\n")
