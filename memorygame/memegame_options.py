import pygame
import random
import time
import sqlite3
import matplotlib.pyplot as plt

# Initialize pygame
pygame.init()

# Set up display
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cognitive Improvement Games")
#Constants for Whack-a-mole
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600  # Increased height to accommodate the score display
GRID_SIZE = 4
CELL_SIZE = 150
MOLE_SIZE = 100
GRID_SPACING = 10  # Space between the tiles
BACKGROUND_COLOR = (255, 255, 255)
HOLE_COLOR = (139, 69, 19)
FPS = 30
MOLE_TIME = 1  # Time a mole stays up in seconds
GAME_TIME = 60  # Total game time in seconds
#Constants for Jigsaw Puzzle
GRID_SIZE = 4
TILE_SIZE = SCREEN_WIDTH // GRID_SIZE
# Font
font = pygame.font.SysFont('arial', 12)

# Clock
clock = pygame.time.Clock()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Whack-a-Mole")
# Load images
MOLE_IMAGE_PATH = 'mole.png'  # Replace this with the path to your mole image file
HAMMER_IMAGE_PATH = 'hammer.png'  # Replace this with the path to your hammer image file
mole_image = pygame.image.load(MOLE_IMAGE_PATH)
mole_image = pygame.transform.scale(mole_image, (MOLE_SIZE, MOLE_SIZE))
hammer_image = pygame.image.load(HAMMER_IMAGE_PATH)
hammer_image = pygame.transform.scale(hammer_image, (50, 50))  # Adjust size as needed
# Font
font = pygame.font.SysFont('arial', 24)
# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define fonts
#font = pygame.font.SysFont(None, 40)

# Card settings for Memory Matching Game
CARD_WIDTH = 100
CARD_HEIGHT = 100
GAP = 10

# Card values (pairs of numbers for matching)
CARD_VALUES = [1, 2, 3, 4, 5, 6, 7, 8] * 2
random.shuffle(CARD_VALUES)

# Create card positions
cards = []
for i in range(4):  # 4 rows
    for j in range(4):  # 4 columns
        x = j * (CARD_WIDTH + GAP) + GAP
        y = i * (CARD_HEIGHT + GAP) + GAP + 100
        cards.append({"value": CARD_VALUES.pop(), "rect": pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT), "flipped": False, "matched": False})

# Initialize game variables
flipped_cards = []
score = 0
start_time = time.time()
scores = []  # List to track all scores
times = []   # List to track all completion times

# Database setup
conn = sqlite3.connect('memory_game.db')
c = conn.cursor()

# Create the table with the correct schema
c.execute('''CREATE TABLE IF NOT EXISTS game_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT, score INTEGER, completion_time INTEGER)''')
conn.commit()

# Helper functions
def draw_text(text, color, x, y):
    message = font.render(text, True, color)
    screen.blit(message, (x, y))

def draw_cards():
    for card in cards:
        if card["flipped"] or card["matched"]:
            pygame.draw.rect(screen, WHITE, card["rect"])
            value_text = font.render(str(card["value"]), True, BLACK)
            screen.blit(value_text, (card["rect"].x + CARD_WIDTH // 4, card["rect"].y + CARD_HEIGHT // 4))
        else:
            pygame.draw.rect(screen, GREEN, card["rect"])

def reset_game():
    global cards, flipped_cards, score, start_time
    CARD_VALUES.extend([1, 2, 3, 4, 5, 6, 7, 8] * 2)
    random.shuffle(CARD_VALUES)
    cards = []
    for i in range(4):
        for j in range(4):
            x = j * (CARD_WIDTH + GAP) + GAP
            y = i * (CARD_HEIGHT + GAP) + GAP + 100
            cards.append({"value": CARD_VALUES.pop(), "rect": pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT), "flipped": False, "matched": False})
    flipped_cards = []
    score = 0
    start_time = time.time()  # Reset the timer
    
def log_game_data(score, completion_time):
    try:
        print(f"Logging data: Score = {score}, Completion Time = {completion_time}")
        print(f"Data types: Score = {type(score)}, Completion Time = {type(completion_time)}")
        print(f"Inserting into database: (score: {score}, completion_time: {completion_time})")
        c.execute("INSERT INTO game_data (score, completion_time) VALUES (?, ?)", (score, completion_time))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def display_game_data():
    try:
        c.execute("SELECT * FROM game_data")
        rows = c.fetchall()
        screen.fill(BLACK)
        y = 50
        for row in rows:
            draw_text(f"Game {row[0]}: Score = {row[1]}, Time = {row[2]}s", WHITE, 50, y)
            y += 40
        pygame.display.update()
        time.sleep(5)
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def plot_progress():
    try:
        c.execute("SELECT * FROM game_data")
        rows = c.fetchall()
        game_ids = [row[0] for row in rows]
        times = [row[2] for row in rows]

        # Debug prints
        print("Fetched game data:", rows)
        print("Game IDs:", game_ids)
        print("Completion Times:", times)

        scores = [row[1] for row in rows]

        plt.figure(figsize=(10, 6))

        # Plot times
        plt.plot(game_ids, times, marker='o', linestyle='-', color='r', label='Completion Time (s)')
        
        # Plot scores
        plt.plot(game_ids, scores, marker='x', linestyle='--', color='b', label='Score')

        # Adjust axes dynamically
        plt.title('Game Progress Over Time')
        plt.xlabel('Game ID')
        plt.ylabel('Performance Metrics')
        plt.xticks(game_ids)  # Ensure all game IDs are shown
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

    # After plotting, show the popup message with options
    show_popup_message("Press R to Replay\nQ to Quit\nD to Display Data\nP to Plot Progress")

def show_popup_message(message):
    popup_width = 500
    popup_height = 300
    popup_x = (WINDOW_WIDTH - popup_width) // 2
    popup_y = (WINDOW_HEIGHT - popup_height) // 2
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    
    pygame.draw.rect(screen, BLUE, popup_rect)
    message_lines = message.split('\n')
    for i, line in enumerate(message_lines):
        text_surface = font.render(line, True, RED)
        text_rect = text_surface.get_rect(center=(popup_x + popup_width // 2, popup_y + 50 + i * 40))
        screen.blit(text_surface, text_rect)
    pygame.display.update()

# Main menu
def main_menu():
    screen.fill(BLACK)
    draw_text("Press 1 to Play Memory Game", WHITE, 200, 200)
    draw_text("Press 2 to Play Whack-a-Mole", WHITE, 200, 300)
    draw_text("Press 3 to Play Solve a Puzzle", WHITE, 200, 400)
    draw_text("Press Q to Quit", WHITE, 200, 500)
    pygame.display.update()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # Clear the database at the beginning of the game to start fresh
                    c.execute("DELETE FROM game_data")
                    c.execute("DELETE FROM sqlite_sequence WHERE name='game_data'")
                    conn.commit()
                    waiting_for_input = False
                    game_loop()
                elif event.key == pygame.K_2:
                    waiting_for_input = False
                    whack_a_mole()
                elif event.key == pygame.K_3:
                    waiting_for_input = False
                    solve_a_puzzle()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Game loop for Memory Matching Game
def game_loop():
    global running, score, start_time, flipped_cards
    running = True
    game_completed = False
    while running:
        screen.fill(BLACK)
        elapsed_time = int(time.time() - start_time)

        # Right-aligned scoreboard
        right_x = WINDOW_WIDTH - 200
        draw_text(f"Score: {score}", WHITE, right_x, 10)
        draw_text(f"Time: {elapsed_time}s", WHITE, right_x, 50)
        if times:
            draw_text(f"Best Time: {min(times)}s", WHITE, right_x, 90)

        # Draw cards
        draw_cards()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and len(flipped_cards) < 2:
                pos = pygame.mouse.get_pos()
                for card in cards:
                    if card["rect"].collidepoint(pos) and not card["flipped"] and not card["matched"]:
                        card["flipped"] = True
                        card["flipped"] = True
                        flipped_cards.append(card)
                        break

        # Check for matches
        if len(flipped_cards) == 2:
            if flipped_cards[0]["value"] == flipped_cards[1]["value"]:
                flipped_cards[0]["matched"] = True
                flipped_cards[1]["matched"] = True
                score += 1
            else:
                flipped_cards[0]["flipped"] = False
                flipped_cards[1]["flipped"] = False
            flipped_cards = []

        # Check if the game is over
        if all(card["matched"] for card in cards) and not game_completed:
            completion_time = int(time.time() - start_time)
            scores.append(score)
            times.append(completion_time)  # Add completion time to the times list
            log_game_data(score, completion_time)  # Log game data to the database
            game_completed = True
            show_popup_message("You Win!\nPress R to Replay\nQ to Quit\nD to Display Data\nP to Plot Progress\nM to Main Menu")
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            reset_game()
                            game_completed = False
                            waiting_for_input = False
                        elif event.key == pygame.K_q:
                            running = False
                            waiting_for_input = False
                            # Clear the database and reset the primary key when quitting
                            c.execute("DELETE FROM game_data")
                            c.execute("DELETE FROM sqlite_sequence WHERE name='game_data'")
                            conn.commit()
                        elif event.key == pygame.K_d:
                            display_game_data()
                            reset_game()
                            game_completed = False
                            show_popup_message("Press R to Replay\nQ to Quit\nP to Plot Progress\nM to Main Menu")
                            waiting_for_input = False
                        elif event.key == pygame.K_p:
                            plot_progress()
                            reset_game()
                            game_completed = False
                            show_popup_message("Press R to Replay\nQ to Quit\nD to Display Data\nM to Main Menu")
                            waiting_for_input = False
                        elif event.key == pygame.K_m:
                            running = False
                            waiting_for_input = False
                            main_menu()

        pygame.display.update()

    pygame.quit()
    conn.close()


def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * (CELL_SIZE + GRID_SPACING)
            y = row * (CELL_SIZE + GRID_SPACING)
            pygame.draw.rect(screen, HOLE_COLOR, (x, y, CELL_SIZE, CELL_SIZE))

def draw_mole(mole_position):
    row, col = mole_position
    x = col * (CELL_SIZE + GRID_SPACING) + (CELL_SIZE - MOLE_SIZE) // 2
    y = row * (CELL_SIZE + GRID_SPACING) + (CELL_SIZE - MOLE_SIZE) // 2
    screen.blit(mole_image, (x, y))
def get_cell_from_mouse_pos(pos):
    x, y = pos
    col = x // (CELL_SIZE + GRID_SPACING)
    row = y // (CELL_SIZE + GRID_SPACING)
    return row, col
# Whack-a-Mole game
def whack_a_mole():
    # Initialize variables
    mole_visible = False
    mole_position = (0, 0)
    mole_time = 1  # Time a mole stays up in seconds
    score = 0
    start_time = time.time()
    last_mole_time = time.time()
    running = True

    while running:
        # Calculate elapsed time
        current_time = time.time()
        elapsed_time = current_time - start_time
        remaining_time = GAME_TIME - elapsed_time
        
        # End game when time runs out
        if remaining_time <= 0:
            running = False

        # Fill the screen with the background color
        screen.fill(BLACK)

        # Draw the grid (holes for the moles to pop up)
        draw_grid()

        # Show the mole if it's time for it to pop up
        if current_time - last_mole_time > mole_time:
            mole_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            last_mole_time = current_time
            mole_visible = True

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mole_visible:
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_cell = get_cell_from_mouse_pos(mouse_pos)
                    if clicked_cell == mole_position:
                        score += 1
                        mole_visible = False

        # Draw the mole if visible
        if mole_visible:
            draw_mole(mole_position)

        # Display the remaining time and score
        time_text = font.render(f"Time: {int(remaining_time)}s", True, WHITE)
        screen.blit(time_text, (10, SCREEN_HEIGHT - 100))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, SCREEN_HEIGHT - 50))

        # Draw the hammer cursor
        mouse_pos = pygame.mouse.get_pos()
        hammer_rect = hammer_image.get_rect(center=mouse_pos)
        screen.blit(hammer_image, hammer_rect.topleft)

        # Update the screen
        pygame.display.flip()
        
        # Control the game speed (frames per second)
        clock.tick(FPS)

    # Once the game ends, log the score and show the message
    completion_time = int(time.time() - start_time)
    scores.append(score)
    times.append(completion_time)
    log_game_data(score, completion_time)
    
    # Show the popup message with options
    show_popup_message("Game Over! Press R to Replay\nQ to Quit\nD to Display Data\nP to Plot Progress\nM to Main Menu")

    # Wait for the player to choose an option
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    whack_a_mole()  # Restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_d:
                    display_game_data()
                    show_popup_message("Press R to Replay\nQ to Quit\nP to Plot Progress\nM to Main Menu")
                    waiting_for_input = False
                elif event.key == pygame.K_p:
                    plot_progress()
                    show_popup_message("Press R to Replay\nQ to Quit\nD to Display Data\nM to Main Menu")
                    waiting_for_input = False
                elif event.key == pygame.K_m:
                    main_menu()
                    waiting_for_input = False


                    main_menu()

# Solve a Puzzle game
    
# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jigsaw Puzzle")

# Load image and split it into tiles
def load_image(path):
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    return image

def get_tiles(image):
    tiles = []
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            tile = image.subsurface(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            tiles.append((tile, row, col))  # Store tile and its position
    return tiles

# Shuffle the tiles
def shuffle_tiles(tiles):
    shuffled = tiles[:]
    random.shuffle(shuffled)
    return shuffled

# Draw the tiles on the screen
def draw_tiles(tiles):
    for i, (tile, _, _) in enumerate(tiles):
        row = i // GRID_SIZE
        col = i % GRID_SIZE
        pos_x = col * TILE_SIZE
        pos_y = row * TILE_SIZE
        screen.blit(tile, (pos_x, pos_y))

# Swap tiles
def swap_tiles(tiles, idx1, idx2):
    tiles[idx1], tiles[idx2] = tiles[idx2], tiles[idx1]

# Check if the puzzle is solved
def is_solved(tiles):
    for i, (tile, original_row, original_col) in enumerate(tiles):
        row = i // GRID_SIZE
        col = i % GRID_SIZE
        if row != original_row or col != original_col:
            return False
    return True

# Main game loop
def solve_a_puzzle():
    image = load_image('rockymountain.jpeg')  # Provide the path to your image
    tiles = get_tiles(image)
    shuffled_tiles = shuffle_tiles(tiles)

    running = True
    selected_tile = None
    dragging = False
    drag_offset_x = 0
    drag_offset_y = 0

    while running:
        screen.fill(WHITE)

        # Draw the tiles on the screen
        draw_tiles(shuffled_tiles)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // TILE_SIZE, y // TILE_SIZE
                selected_tile = row * GRID_SIZE + col
                if selected_tile is not None:
                    dragging = True
                    drag_offset_x = x - (col * TILE_SIZE)
                    drag_offset_y = y - (row * TILE_SIZE)

            if event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    dragging = False
                    # Place the tile back into its new position
                    x, y = pygame.mouse.get_pos()
                    target_col, target_row = x // TILE_SIZE, y // TILE_SIZE
                    target_idx = target_row * GRID_SIZE + target_col
                    if target_idx != selected_tile:
                        swap_tiles(shuffled_tiles, selected_tile, target_idx)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Check if the puzzle is solved
                    if is_solved(shuffled_tiles):
                        print("Puzzle Solved!")
                        running = False

        # If dragging, render the selected tile at the mouse position
        if dragging and selected_tile is not None:
            tile, _, _ = shuffled_tiles[selected_tile]
            x, y = pygame.mouse.get_pos()
            screen.blit(tile, (x - drag_offset_x, y - drag_offset_y))

        pygame.display.update()
        pygame.time.Clock().tick(FPS)


# Start the main menu and game loop
while True:
    main_menu()
