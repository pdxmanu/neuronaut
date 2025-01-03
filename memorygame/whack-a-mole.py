import pygame
import random
import time

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700  # Increased height to accommodate the score display
GRID_SIZE = 4
CELL_SIZE = 150
MOLE_SIZE = 100
GRID_SPACING = 10  # Space between the tiles
BACKGROUND_COLOR = (255, 255, 255)
HOLE_COLOR = (139, 69, 19)
FPS = 30
MOLE_TIME = 1  # Time a mole stays up in seconds
GAME_TIME = 60  # Total game time in seconds

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
font = pygame.font.SysFont('arial', 36)

# Clock
clock = pygame.time.Clock()

# Initialize variables
score = 0
mole_visible = False
last_mole_time = time.time()
start_time = time.time()

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

# Game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)
    draw_grid()

    current_time = time.time()
    elapsed_time = current_time - start_time
    remaining_time = GAME_TIME - elapsed_time
    if remaining_time <= 0:
        running = False

    # Show the mole at random intervals
    if current_time - last_mole_time > MOLE_TIME:
        mole_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        last_mole_time = current_time
        mole_visible = True

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

    if mole_visible:
        draw_mole(mole_position)

    # Display remaining time
    time_text = font.render(f"Time: {int(remaining_time)}s", True, (0, 0, 0))
    screen.blit(time_text, (10, SCREEN_HEIGHT - 100))

    # Display score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, SCREEN_HEIGHT - 50))

    # Draw the hammer cursor
    mouse_pos = pygame.mouse.get_pos()
    hammer_rect = hammer_image.get_rect(center=mouse_pos)
    screen.blit(hammer_image, hammer_rect.topleft)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

