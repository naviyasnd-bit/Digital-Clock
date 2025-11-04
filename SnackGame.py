from tkinter import *
import random

# --- Global Constants (Visible in 1000143511.jpg) ---
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100 # Delay in milliseconds for the next game turn
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"  # Green
FOOD_COLOR = "#FF0000"   # Red
BACKGROUND_COLOR = "#000000" # Black

score = 0
direction = 'down' # Initial direction

class Snake:
    """Represents the snake object in the game."""
    def __init__(self, canvas):
        self.canvas = canvas
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Initialize snake body (Visible in 1000143512.jpg)
        for i in range(0, BODY_PARTS):
            # Start all segments at (0, 0)
            self.coordinates.append([0, 0]) 
        
        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, 
                fill=SNAKE_COLOR, 
                tag="snake"
            )
            self.squares.append(square)

class Food:
    """Represents the food object in the game."""
    def __init__(self, canvas):
        self.canvas = canvas
        # Randomly place food on the grid (multiples of SPACE_SIZE)
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        
        self.coordinates = [x, y]
        
        # Draw the food as an oval (Visible in 1000143515.jpg)
        self.canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, 
            fill=FOOD_COLOR, 
            tag="food"
        )

# --- Game Functions ---

def next_turn(snake, food, canvas, label):
    """
    Handles the snake's movement, checks for collisions and food consumption.
    This function is called repeatedly by the main game loop.
    """
    global direction, score

    # Get the current head position
    x, y = snake.coordinates[0]

    # Calculate the new head position based on direction (Visible in 1000143512.jpg)
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # 1. Update the snake's coordinates list
    snake.coordinates.insert(0, (x, y))

    # 2. Create a new square for the head
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, 
        fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    # Check for food consumption (Visible in 1000143513.jpg)
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score:{}".format(score)) # Update score label
        
        canvas.delete("food") # Remove the old food
        food = Food(canvas) # Create new food
    else:
        # If no food is eaten, delete the tail segment (Visible in 1000143513.jpg)
        del snake.coordinates[-1] 
        canvas.delete(snake.squares[-1]) # Remove the tail square from canvas
        del snake.squares[-1]

    # Check for game over (collisions)
    if check_collisions(snake):
        game_over(canvas)
    else:
        # Schedule the next turn (main game loop)
        canvas.after(SPEED, next_turn, snake, food, canvas, label)

def change_direction(new_direction):
    """Prevents the snake from immediately reversing direction (Visible in 1000143514.jpg)."""
    global direction
    
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    """Checks for collision with wall or self."""
    x, y = snake.coordinates[0] # Head coordinates
    
    # Wall collision (Visible in 1000143514.jpg - 'if x < 0 or x >= GAME_WIDTH')
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    # Self-collision
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
            
    return False

def game_over(canvas):
    """Displays the Game Over message (Visible in 1000143514.jpg and 1000143515.jpg)."""
    canvas.delete(ALL)
    # Display "GAME OVER" text
    canvas.create_text(
        canvas.winfo_width() / 2, 
        canvas.winfo_height() / 2, 
        font=('consolas', 70), 
        text="GAME OVER", 
        fill="red", 
        tag="gameover"
    )

def main():
    """Sets up the Tkinter window and starts the game."""
    window = Tk()
    window.title("Snake Game")
    window.resizable(False, False) # Prevent window resizing

    # Create the score label (Visible in 1000143515.jpg)
    label = Label(
        window, 
        text="Score:{}".format(score), 
        font=('consolas', 40)
    )
    label.pack()

    # Create the drawing canvas
    canvas = Canvas(
        window, 
        bg=BACKGROUND_COLOR, 
        height=GAME_HEIGHT, 
        width=GAME_WIDTH
    )
    canvas.pack()

    # Center the window on the screen (Visible in 1000143516.jpg)
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = int((screen_width / 2) - (GAME_WIDTH / 2)) # Use GAME_WIDTH/HEIGHT for initial centering
    y = int((screen_height / 2) - (GAME_HEIGHT / 2))
    
    window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}+{x}+{y}") # Set window size and position

    # Create game elements
    snake = Snake(canvas)
    food = Food(canvas)

    # Bind arrow keys to change_direction function (Visible in 1000143516.jpg)
    window.bind('<Left>', lambda event: change_direction('left'))
    window.bind('<Right>', lambda event: change_direction('right'))
    window.bind('<Up>', lambda event: change_direction('up'))
    window.bind('<Down>', lambda event: change_direction('down'))
    
    # Start the game loop
    next_turn(snake, food, canvas, label) 

    window.mainloop()

# Execute the main function
if __name__ == "__main__":
    main()