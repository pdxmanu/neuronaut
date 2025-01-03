
import pygame
import random
import time
import sqlite3
import matplotlib.pyplot as plt

# Initialize pygame
pygame.init()

# Set up display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Attention Games")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (169, 169, 169)

# Define fonts
font = pygame.font.SysFont(None, 40)

# Database setup
conn = sqlite3.connect('attention_games.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS game_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT, game_type TEXT, score INTEGER, completion_time INTEGER)''')
conn.commit()

# Helper Functions
def draw_text(text, color, x, y, center=False):
    message = font.render(text, True, color)
    if center:
        text_rect = message.get_rect(center=(x, y))
        screen.blit(message, text_rect.topleft)
    else:
        screen.blit(message, (x, y))

def log_game_data(game_type, score, completion_time):
    c.execute("INSERT INTO game_data (game_type, score, completion_time) VALUES (?, ?, ?)", 
              (game_type, score, completion_time))
    conn.commit()

def display_game_data(game_type=None):
    screen.fill(BLACK)
    if game_type:
        c.execute("SELECT * FROM game_data WHERE game_type = ?", (game_type,))
    else:
        c.execute("SELECT * FROM game_data")
    rows = c.fetchall()
    y = 50
    for row in rows:
        draw_text(f"Game {row[0]}: {row[1]} - Score: {row[2]}, Time: {row[3]}s", WHITE, 50, y)
        y += 40
    pygame.display.update()
    time.sleep(5)

def plot_progress(game_type):
    c.execute("SELECT * FROM game_data WHERE game_type = ?", (game_type,))
    rows = c.fetchall()
    game_ids = [row[0] for row in rows]
    scores = [row[2] for row in rows]
    times = [row[3] for row in rows]

    plt.figure(figsize=(10, 6))
    plt.plot(game_ids, scores, marker='o', linestyle='-', label='Score', color='blue')
    plt.plot(game_ids, times, marker='x', linestyle='--', label='Completion Time (s)', color='red')
    plt.title(f'Progress for {game_type}')
    plt.xlabel('Game ID')
    plt.ylabel('Performance Metrics')
    plt.legend()
    plt.grid(True)
    plt.show()

# Main Menu
def main_menu():
    screen.fill(BLACK)
    draw_text("Select a Game:", WHITE, 400, 100, center=True)
    draw_text("1. Memory Game", GREEN, 300, 200)
    draw_text("2. Spot the Difference", GREEN, 300, 250)
    draw_text("3. Whack-a-Mole", GREEN, 300, 300)
    draw_text("4. Puzzle Game", GREEN, 300, 350)
    draw_text("Press Q to Quit", RED, 300, 400)
    pygame.display.update()
    
    # Wait for the user to select a game or quit
    selected_game = None
    while selected_game is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                conn.close()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_game = "memory"
                elif event.key == pygame.K_2:
                    selected_game = "spot_difference"
                elif event.key == pygame.K_3:
                    selected_game = "whack_a_mole"
                elif event.key == pygame.K_4:
                    selected_game = "puzzle"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    conn.close()
                    exit()
    
    return selected_game

# Memory Game Setup (new function)
def setup_memory_game():
    """Sets up the memory game by creating a shuffled set of cards."""
    values = ["A", "B", "C", "D", "E", "F", "G", "H", "A", "B", "C", "D", "E", "F", "G", "H"]
    random.shuffle(values)
    
    cards = []
    card_width = 100
    card_height = 100
    margin = 20
    rows = 4
    cols = 4
    for row in range(rows):
        for col in range(cols):
            x = col * (card_width + margin) + 100
            y = row * (card_height + margin) + 100
            value = values.pop()
            card = {"rect": pygame.Rect(x, y, card_width, card_height), "value": value, "flipped": False, "matched": False}
            cards.append(card)
    
    return cards

# Memory Game Logic
def memory_game():
    score = 0
    start_time = time.time()
    game_completed = False
    flipped_cards = []
    cards = setup_memory_game()  # Set up the memory game cards
    
    while not game_completed:
        screen.fill(BLACK)
        elapsed_time = int(time.time() - start_time)

        # Right-aligned scoreboard
        right_x = WINDOW_WIDTH - 200
        draw_text(f"Score: {score}", WHITE, right_x, 10)
        draw_text(f"Time: {elapsed_time}s", WHITE, right_x, 50)

        # Draw cards
        for card in cards:
            if card["flipped"] or card["matched"]:
                pygame.draw.rect(screen, WHITE, card["rect"])
                draw_text(card["value"], BLACK, card["rect"].centerx, card["rect"].centery, center=True)
            else:
                pygame.draw.rect(screen, GRAY, card["rect"])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                conn.close()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and len(flipped_cards) < 2:
                pos = pygame.mouse.get_pos()
                for card in cards:
                    if card["rect"].collidepoint(pos) and not card["flipped"] and not card["matched"]:
                        card["flipped"] = True
                        flipped_cards.append(card)
                        break

        # Check for matches
        if len(flipped_cards) == 2:
            pygame.time.delay(500)
            if flipped_cards[0]["value"] == flipped_cards[1]["value"]:
                flipped_cards[0]["matched"] = True
                flipped_cards[1]["matched"] = True
                score += 1
            else:
                flipped_cards[0]["flipped"] = False
                flipped_cards[1]["flipped"] = False
            flipped_cards = []

        # Check if the game is over
        if all(card["matched"] for card in cards):
            completion_time = int(time.time() - start_time)
            log_game_data("memory", score, completion_time)  # Log game data to the database
            game_completed = True
            display_game_data("memory")

# Spot the Difference Game
def spot_the_difference_game():
    # Load two images to compare
    img1 = pygame.image.load('image1.png')
    img2 = pygame.image.load('image2.png')
    img_rect = img1.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    differences = [(100, 100), (150, 150), (200, 200)]  # Example coordinates of differences
    found_differences = []
    
    # Game loop
    score = 0
    start_time = time.time()
    game_completed = False

    while not game_completed:
        screen.fill(BLACK)
        elapsed_time = int(time.time() - start_time)

        # Display images
        screen.blit(img1, img_rect)
        for diff in differences:
            if diff in found_differences:
                pygame.draw.circle(screen, GREEN, diff, 10)
            else:
                pygame.draw.circle(screen, RED, diff, 10)
        
        # Display Score and Time
        right_x = WINDOW_WIDTH - 200
        draw_text(f"Score: {score}", WHITE, right_x, 10)
        draw_text(f"Time: {elapsed_time}s", WHITE, right_x, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                conn.close()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for diff in differences:
                    if pygame.Rect(diff[0] - 10, diff[1] - 10, 20, 20).collidepoint(pos) and diff not in found_differences:
                        found_differences.append(diff)
                        score += 1
                        break

        # Check if all differences are found
        if len(found_differences) == len(differences):
            completion_time = int(time.time() - start_time)
            log_game_data("spot_difference", score, completion_time)  # Log game data to the database
            game_completed = True
            display_game_data("spot_difference")

# Whack-a-Mole Game
def whack_a_mole_game():
    mole_radius = 40
    num_holes = 9  # 3x3 grid
    mole_positions = [(100, 100), (300, 100), (500, 100),
                      (100, 300), (300, 300), (500, 300),
                      (100, 500), (300, 500), (500, 500)]
    mole = None
    score = 0
    start_time = time.time()
    game_completed = False

    while not game_completed:
        screen.fill(BLACK)
        elapsed_time = int(time.time() - start_time)

        # Randomly show a mole
        if mole is None or random.random() < 0.05:  # Mole appears at random intervals
            mole = random.choice(mole_positions)
        
        # Draw holes
        for pos in mole_positions:
            pygame.draw.circle(screen, GRAY, pos, mole_radius)
        
        # Draw mole
        if mole:
            pygame.draw.circle(screen, GREEN, mole, mole_radius)
        
        # Display Score and Time
        right_x = WINDOW_WIDTH - 200
        draw_text(f"Score: {score}", WHITE, right_x, 10)
        draw_text(f"Time: {elapsed_time}s", WHITE, right_x, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                conn.close()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if mole and pygame.Rect(mole[0] - mole_radius, mole[1] - mole_radius, 2 * mole_radius, 2 * mole_radius).collidepoint(pos):
                    score += 1
                    mole = None  # Mole disappears after being hit

        # Check if the game is over (for example, after a certain time limit)
        if elapsed_time > 60:  # End after 60 seconds
            completion_time = int(time.time() - start_time)
            log_game_data("whack_a_mole", score, completion_time)  # Log game data to the database
            game_completed = True
            display_game_data("whack_a_mole")

# Puzzle Game
def puzzle_game():
    # Example: Sliding puzzle with a 3x3 grid (8-puzzle)
    puzzle = list(range(9))  # Numbers from 0 to 8
    random.shuffle(puzzle)
    grid_size = 3
    tile_size = 100
    empty_tile = puzzle.index(0)  # The empty space in the puzzle

    # Function to swap tiles
    def swap_tiles(puzzle, idx1, idx2):
        puzzle[idx1], puzzle[idx2] = puzzle[idx2], puzzle[idx1]

    # Function to draw the puzzle grid
    def draw_puzzle(puzzle):
        for i in range(9):
            x = (i % grid_size) * tile_size
            y = (i // grid_size) * tile_size
            if puzzle[i] != 0:
                draw_text(str(puzzle[i]), WHITE, x + tile_size // 2, y + tile_size // 2, center=True)
            pygame.draw.rect(screen, WHITE, pygame.Rect(x, y, tile_size, tile_size), 2)
    
    # Game loop
    score = 0
    start_time = time.time()
    game_completed = False

    while not game_completed:
        screen.fill(BLACK)
        elapsed_time = int(time.time() - start_time)

        # Draw the puzzle
        draw_puzzle(puzzle)

        # Display Score and Time
        right_x = WINDOW_WIDTH - 200
        draw_text(f"Score: {score}", WHITE, right_x, 10)
        draw_text(f"Time: {elapsed_time}s", WHITE, right_x, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                conn.close()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = pos[1] // tile_size
                col = pos[0] // tile_size
                clicked_tile = row * grid_size + col

                # Check if a tile can be swapped with the empty space
                if (clicked_tile == empty_tile - 1 and col > 0) or (clicked_tile == empty_tile + 1 and col < grid_size - 1) or \
                   (clicked_tile == empty_tile - grid_size and row > 0) or (clicked_tile == empty_tile + grid_size and row < grid_size - 1):
                    swap_tiles(puzzle, clicked_tile, empty_tile)
                    empty_tile = clicked_tile

        # Check if the puzzle is solved
        if puzzle == list(range(9)):
            completion_time = int(time.time() - start_time)
            log_game_data("puzzle", score, completion_time)  # Log game data to the database
            game_completed = True
            display_game_data("puzzle")

# Game Loop
while True:
    game_type = main_menu()
    if game_type == "memory":
        memory_game()
    elif game_type == "spot_difference":
        spot_the_difference_game()
    elif game_type == "whack_a_mole":
        whack_a_mole_game()
    elif game_type == "puzzle":
        puzzle_game()
