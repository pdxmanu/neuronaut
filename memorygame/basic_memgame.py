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
pygame.display.set_caption("Memory Matching Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define fonts
font = pygame.font.SysFont(None, 40)

# Card settings
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

# Check if the 'completion_time' column exists, and add it if it doesn't
c.execute("PRAGMA table_info(game_data)")
columns = [column[1] for column in c.fetchall()]
if 'completion_time' not in columns:
    c.execute("ALTER TABLE game_data ADD COLUMN completion_time INTEGER")

c.execute('''CREATE TABLE IF NOT EXISTS game_data
             (id INTEGER PRIMARY KEY, score INTEGER, completion_time INTEGER)''')
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
    start_time = time.time()

def log_game_data(score, completion_time):
    c.execute("INSERT INTO game_data (score, completion_time) VALUES (?, ?)", (score, completion_time))
    conn.commit()

def display_game_data():
    c.execute("SELECT * FROM game_data")
    rows = c.fetchall()
    screen.fill(BLACK)
    y = 50
    for row in rows:
        draw_text(f"Game {row[0]}: Score = {row[1]}, Time = {row[2]}s", WHITE, 50, y)
        y += 40
    pygame.display.update()
    time.sleep(5)

def plot_progress():
    c.execute("SELECT * FROM game_data")
    rows = c.fetchall()
    game_ids = [row[0] for row in rows]
    scores = [row[1] for row in rows]
    times = [row[2] for row in rows]

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(game_ids, scores, marker='o', linestyle='-', color='b')
    plt.title('Scores Over Time')
    plt.xlabel('Game ID')
    plt.ylabel('Score')

    plt.subplot(1, 2, 2)
    plt.plot(game_ids, times, marker='o', linestyle='-', color='r')
    plt.title('Completion Time Over Time')
    plt.xlabel('Game ID')
    plt.ylabel('Time (s)')

    plt.tight_layout()
    plt.show()

# Main menu
def main_menu():
    screen.fill(BLACK)
    draw_text("Press S to Start Game", WHITE, 200, 200)
    draw_text("Press D to Display Game Data", WHITE, 200, 300)
    draw_text("Press P to Plot Progress", WHITE, 200, 400)
    pygame.display.update()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    waiting_for_input = False
                elif event.key == pygame.K_d:
                    display_game_data()
                    waiting_for_input = False
                elif event.key == pygame.K_p:
                    plot_progress()
                    waiting_for_input = False

# Game loop
def game_loop():
    global running, score, start_time, flipped_cards
    running = True
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
            scores.append(score)  # Add current score to the scores list
            times.append(completion_time)  # Add completion time to the times list
            log_game_data(score, completion_time)  # Log game data to the database
            draw_text("You Win! Press R to Replay, Q to Quit, D to Display Data, or P to Plot Progress", RED, 50, WINDOW_HEIGHT // 2)
            pygame.display.update()
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting_for_input = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            reset_game()
                            waiting_for_input = False
                        elif event.key == pygame.K_q:
                            running = False
                            waiting_for_input = False
                        elif event.key == pygame.K_d:
                            display_game_data()
                            waiting_for_input = False
                        elif event.key == pygame.K_p:
                            plot_progress()
                            waiting_for_input = False

        pygame.display.update()

    pygame.quit()
    conn.close()

# Start the main menu and game loop
while True:
    main_menu()
    game_loop()
