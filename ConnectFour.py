import numpy as np
import pygame
import sys

# --- 1. Constants and Setup ---
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

# Define Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Calculate Screen Dimensions
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE # +1 for the top move indicator row
SIZE = (width, height)


# --- 2. Game Logic Functions ---

def create_board():
    """Initializes the game board using NumPy."""
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    """Places the piece on the board."""
    board[row][col] = piece

def is_valid_location(board, col):
    """Checks if the top spot in a column is empty."""
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    """Finds the lowest empty row in the given column."""
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    """Flips and prints the board to show row 0 at the bottom."""
    print(np.flip(board, 0))

def winning_move(board, piece):
    """Checks for 4-in-a-row horizontally, vertically, and diagonally."""
    # Check horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals (bottom-left to top-right)
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals (top-left to bottom-right)
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    return False


# --- 3. Pygame Drawing Functions (Fixing your NameError) ---

def draw_board(board):
    """Draws the blue board and empty circles."""
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # Draw the blue rectangle for the board slot
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            
            # Draw the black circle for the empty slot
            center_x = int(c * SQUARESIZE + SQUARESIZE / 2)
            center_y = int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)
            pygame.draw.circle(screen, BLACK, (center_x, center_y), RADIUS)

    # Draw the pieces that have been dropped
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1: # Player 1 (Red)
                # **FIX for NameError:** The variables for the circle center (posx/posy) are calculated here.
                posx = int(c * SQUARESIZE + SQUARESIZE / 2)
                # The board is flipped, so we adjust r: (ROW_COUNT - 1 - r)
                posy = int(height - (r * SQUARESIZE + SQUARESIZE / 2)) 
                pygame.draw.circle(screen, RED, (posx, posy), RADIUS)
            elif board[r][c] == 2: # Player 2 (Yellow)
                posx = int(c * SQUARESIZE + SQUARESIZE / 2)
                posy = int(height - (r * SQUARESIZE + SQUARESIZE / 2))
                pygame.draw.circle(screen, YELLOW, (posx, posy), RADIUS)
    
    pygame.display.update()


# --- 4. Initialization and Main Game Loop ---

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode(SIZE)
myfont = pygame.font.SysFont("monospace", 75)

board = create_board()
print_board(board)
draw_board(board)

game_over = False
turn = 0  # 0 for Player 1 (Red), 1 for Player 2 (Yellow)

# Main Game Loop
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # Handle mouse movement for the top indicator
        if event.type == pygame.MOUSEMOTION:
            posx = event.pos[0]
            if turn == 0:
                color = RED
            else:
                color = YELLOW
            # Erase the previous indicator
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            # Draw the new indicator (This is where your error likely occurred before!)
            pygame.draw.circle(screen, color, (posx, int(SQUARESIZE/2)), RADIUS)
        
        pygame.display.update()

        # Handle mouse click for dropping a piece
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE)) # Clear indicator

            # --- Player 1 Turn (RED) ---
            if turn == 0:
                posx = event.pos[0]
                col = int(posx / SQUARESIZE)
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 Wins!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True
                
            # --- Player 2 Turn (YELLOW) ---
            else:
                posx = event.pos[0]
                col = int(posx / SQUARESIZE)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 Wins!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        game_over = True

            # Game housekeeping
            print_board(board)
            draw_board(board)

            # Switch turns
            turn += 1
            turn = turn % 2

    # If game over, wait for a click to quit if game