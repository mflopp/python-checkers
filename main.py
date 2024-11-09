# main.py

# importing function to start the game
from game import play_game

def display_menu():
    print("\033c")
    print("Welcome to Checkers!")
    print("Choose a game mode:")
    print("1. 2 Human Players")
    print("2. Human vs Computer")
    print("3. Exit\n")
    
    while True:
        # strip() trims spaces from both sides
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        if choice in ["1", "2", "3"]:
            break
        else:
            print("Invalid input. Please enter 1, 2, or 3.")
    
    if choice == "2":
        while True:
            # capitalize() makes first letter upper case and the rest lower case
            color_choice = input("Choose your color (White or Black): ").strip().capitalize()
            if color_choice in ["White", "Black"]:
                break
            else:
                print("Invalid input. Please enter 'White' or 'Black'.")
        return choice, color_choice
    else:
        return choice, None

def main():
    """
    Main function to start the game.
    """
    choice, color_choice = display_menu()
    if choice == "3":
        print("Exiting the game. Goodbye!\n")
        return
    play_game(choice, color_choice)

if __name__ == "__main__":
    main()
