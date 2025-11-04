# Tic-Tac-Toe Game

def print_board(board):
    """Prints the current state of the Tic-Tac-Toe board."""
    for row in board:
        print("|".join(row))
        print("-" * 5)

def check_winner(board, player):
    """Checks if the specified player has won the game."""
    # Check rows
    for row in board:
        if all(s == player for s in row):
            return True
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def play_game():
    """Main function to run the Tic-Tac-Toe game."""
    # Initialize a 3x3 board with empty spaces
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ['X', 'O']
    current_player_index = 0
    moves_made = 0

    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    # Game loop
    while moves_made < 9:
        current_player = players[current_player_index]
        try:
            # Get user input for move coordinates (row and column)
            row = int(input(f"Player {current_player}, enter your row (0-2): "))
            col = int(input(f"Player {current_player}, enter your column (0-2): "))
            
            # Input validation
            if not (0 <= row <= 2 and 0 <= col <= 2):
                print("Invalid input. Please enter numbers between 0 and 2.")
                continue

            # Check if the spot is empty
            if board[row][col] == " ":
                board[row][col] = current_player
                moves_made += 1
                print_board(board)

                # Check for a winner after the move
                if check_winner(board, current_player):
                    print(f"Player {current_player} wins!")
                    return # End the game
                
                # Switch to the next player
                current_player_index = (current_player_index + 1) % 2
            else:
                print("That spot is already taken! Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # If the loop finishes without a winner
    print("It's a draw!")

# Start the game
play_game()