import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Snake direction constants
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # Add new head to the snake's body
        self.body.insert(0, new_head)

        # If not growing, remove the tail
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction

    def grow_snake(self):
        self.grow = True

    def check_collision(self):
        head_x, head_y = self.body[0]
        if not (0 <= head_x < GRID_WIDTH and 0 <= head_y < GRID_HEIGHT):
            return True
        if len(self.body) != len(set(self.body)):
            return True
        return False

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Function to draw the grid
def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

# Function to draw the snake and food
def draw_objects(snake, food):
    for segment in snake.body:
        pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (food.position[0] * CELL_SIZE, food.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Main game loop
def main():
    snake = Snake()
    food = Food()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)

        if not game_over:
            snake.move()

        if snake.check_collision():
            game_over = True

        if snake.body[0] == food.position:
            snake.grow_snake()
            food.randomize_position()

        screen.fill(BLACK)
        draw_grid()
        draw_objects(snake, food)
        pygame.display.flip()

        clock.tick(10)

if __name__ == "__main__":
    main()