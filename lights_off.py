import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 700, 700
BORDER_SIZE = 100  # Size of the white boundary

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Grid Example')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load background image
welcome_image = pygame.image.load('./welcome.png').convert()
welcome_image = pygame.transform.scale(welcome_image, (WIDTH, HEIGHT))

congratulations_image = pygame.image.load('./congratulations.png').convert()
congratulations_image = pygame.transform.scale(congratulations_image, (WIDTH, HEIGHT))

# Dictionary to store the color of each cell
cell_colors = {}

# Function to draw the grid
def draw_grid(rows, cols, cell_size, total_moves, total_red):
    grid_width = cols * cell_size
    grid_height = rows * cell_size
    for x in range(BORDER_SIZE, BORDER_SIZE + grid_width, cell_size):
        for y in range(BORDER_SIZE, BORDER_SIZE + grid_height, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            color = cell_colors.get((x, y), WHITE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)
    # Draw the black border around the grid
    pygame.draw.rect(screen, BLACK, (BORDER_SIZE, BORDER_SIZE, grid_width, grid_height), 5)

    # Display total moves
    font = pygame.font.SysFont(None, 24)
    moves_text = font.render(f'Moves: {total_moves}', True, BLACK)
    screen.blit(moves_text, (BORDER_SIZE, HEIGHT - 30))

    # Display total red cells
    red_text = font.render(f'Red Cells: {total_red}', True, BLACK)
    screen.blit(red_text, (BORDER_SIZE, HEIGHT - 60))

def toggle(grid_x, grid_y, rows, cols, cell_size, total_moves, total_red):
    # Check if the cell is within the grid boundaries
    if BORDER_SIZE <= grid_x < BORDER_SIZE + cols * cell_size and BORDER_SIZE <= grid_y < BORDER_SIZE + rows * cell_size:
        # Initialize cell color if not already in the dictionary
        if (grid_x, grid_y) not in cell_colors:
            cell_colors[(grid_x, grid_y)] = WHITE
        
        # Toggle the color of the cell
        if cell_colors[(grid_x, grid_y)] == RED:
            cell_colors[(grid_x, grid_y)] = WHITE
            total_red -= 1
        else:
            cell_colors[(grid_x, grid_y)] = RED
            total_red += 1

    return total_red

def draw_input_box(input_rect, font, text):
    pygame.draw.rect(screen, WHITE, input_rect)  # Clear previous text by filling with background color
    pygame.draw.rect(screen, BLACK, input_rect, 2)  # Redraw input box outline
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))


# Homescreen function with input box for grid size
def draw_homescreen():
    screen.blit(welcome_image, (0, 0))
    font = pygame.font.SysFont(None, 48)

    input_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 40)
    input_text = ''
    font_input = pygame.font.SysFont(None, 32)

    pygame.draw.rect(screen, BLACK, input_rect, 2)

    pygame.display.flip()

    while True:
        draw_input_box(input_rect, font_input, input_text)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        cols = int(input_text)
                        rows = cols
                        if ((cols > 30) or (cols <= 1)) :
                            draw_homescreen()
                        return rows, cols
                    except ValueError:
                        pass
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

def draw_exit_screen():
    screen.blit(congratulations_image, (0, 0))
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    running = True
    won = False
    total_moves = 0
    total_red = 0

    while running:
        if not won:
            rows, cols = draw_homescreen()
            cell_size = min((WIDTH - 2 * BORDER_SIZE) // cols, (HEIGHT - 2 * BORDER_SIZE) // rows)

            total_moves = 0
            total_red = 0
            for x in range(BORDER_SIZE, BORDER_SIZE + cols * cell_size, cell_size):
                for y in range(BORDER_SIZE, BORDER_SIZE + rows * cell_size, cell_size):
                    rand_no = random.choice([1, 0])
                    if rand_no == 1:
                        cell_colors[(x, y)] = RED
                        total_red += 1
                    else:
                        cell_colors[(x, y)] = WHITE

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        if ((mouse_x >= (WIDTH - BORDER_SIZE)) or (mouse_y >= (HEIGHT - BORDER_SIZE)) or (mouse_y <= BORDER_SIZE) or (mouse_x <= BORDER_SIZE)) :
                            continue
                        grid_x = ((mouse_x - BORDER_SIZE) // cell_size) * cell_size + BORDER_SIZE
                        grid_y = ((mouse_y - BORDER_SIZE) // cell_size) * cell_size + BORDER_SIZE
                        total_red = toggle(grid_x, grid_y, rows, cols, cell_size, total_moves, total_red)
                        total_red = toggle(grid_x, grid_y + cell_size, rows, cols, cell_size, total_moves, total_red)
                        total_red = toggle(grid_x, grid_y - cell_size, rows, cols, cell_size, total_moves, total_red)
                        total_red = toggle(grid_x - cell_size, grid_y, rows, cols, cell_size, total_moves, total_red)
                        total_red = toggle(grid_x + cell_size, grid_y, rows, cols, cell_size, total_moves, total_red)
                        total_moves += 1

                screen.fill(WHITE)  # Fill the screen with white
                draw_grid(rows, cols, cell_size, total_moves, total_red)

                pygame.display.flip()
                clock.tick(60)

                if total_red == 0:
                    won = True
                    break
        else:
            draw_exit_screen()
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
