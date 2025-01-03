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
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                conn.close()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "memory"
                elif event.key == pygame.K_2:
                    return "spot_difference"
                elif event.key == pygame.K_3:
                    return "whack_a_mole"
                elif event.key == pygame.K_4:
                    return "puzzle"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    conn.close()
                    exit()

# Memory Game
def memory_game():
    # (Code for the memory game here, similar to your provided code)
    pass

# Spot the Difference Game
def spot_the_difference_game():
    # Placeholder for Spot the Difference logic
    pass

# Whack-a-Mole Game
def whack_a_mole_game():
    # Placeholder for Whack-a-Mole logic
    pass

# Puzzle Game
def puzzle_game():
    # Placeholder for Puzzle logic
    pass

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
