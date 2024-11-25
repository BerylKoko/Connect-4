import os
os.environ["SDL_AUDIODRIVER"] = "dummy"  # Use a dummy audio driver
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH = 700
HEIGHT = 600
RADIUS = 40
MARGIN = 5
NUM_COLS = 7
NUM_ROWS = 6
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)

# Set up game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4")

# Create an empty game board (6 rows x 7 columns)
board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# Initialize game variables
current_player = 'R'  # 'R' is red, 'P' is purple
game_over = False

# Draw the game board
def draw_board():
    screen.fill(BLUE)  # Clear the screen
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            pygame.draw.circle(screen, WHITE, (col * (WIDTH // NUM_COLS) + WIDTH // NUM_COLS // 2, 
                                               row * (HEIGHT // NUM_ROWS) + HEIGHT // NUM_ROWS // 2), RADIUS)
            if board[row][col] == 'R':
                pygame.draw.circle(screen, RED, (col * (WIDTH // NUM_COLS) + WIDTH // NUM_COLS // 2, 
                                                 row * (HEIGHT // NUM_ROWS) + HEIGHT // NUM_ROWS // 2), RADIUS - MARGIN)
            elif board[row][col] == 'P':
                pygame.draw.circle(screen, PURPLE, (col * (WIDTH // NUM_COLS) + WIDTH // NUM_COLS // 2, 
                                                    row * (HEIGHT // NUM_ROWS) + HEIGHT // NUM_ROWS // 2), RADIUS - MARGIN)
    pygame.display.update()

# Drop a piece into the column
def drop_piece(col):
    global current_player, game_over

    for row in range(NUM_ROWS - 1, -1, -1):  # Start from bottom
        if board[row][col] == ' ':
            board[row][col] = current_player
            if check_winner(row, col):
                game_over = True
            current_player = 'P' if current_player == 'R' else 'R'  # Switch player
            break

# Check if there is a winner
def check_winner(row, col):
    color = board[row][col]
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonal down-right, Diagonal up-right

    for direction in directions:
        count = 1
        for step in range(1, 4):  # Check one direction
            r = row + direction[0] * step
            c = col + direction[1] * step
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == color:
                count += 1
            else:
                break
        for step in range(1, 4):  # Check the opposite direction
            r = row - direction[0] * step
            c = col - direction[1] * step
            if 0 <= r < NUM_ROWS and 0 <= c < NUM_COLS and board[r][c] == color:
                count += 1
            else:
                break
        if count >= 4:
            return True
    return False

# Display a message when the game is over
def display_winner(winner):
    font = pygame.font.SysFont('Arial', 100, bold=True)  # Big, bold font
    text = font.render(f"{winner} wins!", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center the text
    screen.blit(text, text_rect)
    pygame.display.update()

# Main game loop
def main():
    global game_over

    while True:
        draw_board()

        if game_over:
            winner = "Red" if current_player == 'P' else "Purple"
            display_winner(winner)
            pygame.time.delay(3000)  # Wait for 3 seconds to display the winner message
            game_over = False
            reset_game()
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posX = event.pos[0]
                col = posX // (WIDTH // NUM_COLS)

                if game_over:
                    continue
                drop_piece(col)

        pygame.display.update()

# Reset the game board
def reset_game():
    global board, current_player, game_over
    board = [[' ' for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    current_player = 'R'  # Red starts the game
    game_over = False

if __name__ == "__main__":
    main()
