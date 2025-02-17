import pygame
import random
import os
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 4
TILE_SIZE = SCREEN_WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 30

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
def jigsaw_game_loop():
    image = load_image('rockymountain.jpeg')  # Provide the path to your image
    tiles = get_tiles(image)
    shuffled_tiles = shuffle_tiles(tiles)

    running = True
    selected_tile = None
    dragging = False
    drag_offset_x = 0
    drag_offset_y = 0
    start_time = pygame.time.get_ticks()  # Start time of the game

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

    # Return the time taken to solve the puzzle
    return (pygame.time.get_ticks() - start_time) / 1000  # Return time in seconds

# Run multiple games and track time
def run_multiple_games(num_games=4):
    times = []  # List to store the time taken for each game

    for _ in range(num_games):
        time_taken = jigsaw_game_loop()  # Run the game and get the time taken
        times.append(time_taken)
        replay = input(f"Game completed in {time_taken:.2f} seconds. Do you want to play again? (y/n): ")
        if replay.lower() != 'y':
            break

    # After 2-4 games, chart the times
    chart_times(times)

# Function to plot the time taken for each game
def chart_times(times):
    plt.figure()
    game_numbers = range(1, len(times) + 1)  # Generate game numbers starting from 1
    plt.plot(game_numbers, times, marker='o', linestyle='-', color='b')
    plt.title("Time Taken to Solve Jigsaw Puzzle")
    plt.xlabel("Game Number")
    plt.ylabel("Time (Seconds)")
    plt.xticks(game_numbers)  # Ensure only integer game numbers are shown on the X-axis
    plt.grid(True)  # Add a grid for better visualization
    plt.show()

# Start the game loop for multiple rounds
run_multiple_games(4)  # Run 4 rounds, you can adjust the number of rounds here

# Quit Pygame
pygame.quit()

