import pygame
import time
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Snake and food properties
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
food_spawn = True

# Direction
direction = 'RIGHT'
change_to = direction

# Initial frame rate
framerate = 15

# Score and hunger
score = 0
hunger = 100

# Invincible time
invincible_time = 0

# Maximum snake length
max_snake_length = 10  # Adjust this value as needed

# Enemy Snakes properties
enemy_snakes_snakes = []
num_enemy_snakes = 1  # Adjust the number of enemy_snakes as needed

for _ in range(num_enemy_snakes):
    enemy_snakes = {
        'pos': [400, 300],
        'body': [[400, 300], [390, 300], [380, 300]],  # Initialize with an empty body
        'directions': ['UP', 'DOWN', 'LEFT', 'RIGHT'],
        'direction': random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT']),
        'direction_change_interval': 5,  # Change direction every 5 frames
        'direction_change_counter': 0
    }
    enemy_snakes_snakes.append(enemy_snakes)

# Display Score function
def Your_score(score):
    value = pygame.font.SysFont('comicsans', 30).render("Your Score: " + str(score), True, WHITE)
    window.blit(value, [0, 0])

# Display Score and Hunger function
def display_info(score, hunger):
    score_text = pygame.font.SysFont('comicsans', 30).render("Score: " + str(score), True, WHITE)
    hunger_text = pygame.font.SysFont('comicsans', 30).render("Hunger: " + str(round(hunger, 1)) + "%", True, WHITE)
    window.blit(score_text, [10, 10])
    window.blit(hunger_text, [10, 40])

# Main Function
def gameLoop():
    global direction, change_to
    global snake_pos, snake_body
    global food_pos, food_spawn
    global score, hunger, framerate
    global enemy_snakes_snakes, num_enemy_snakes
    global invincible_time

    # Game Over
    game_over = False
    game_close = False

    while not game_over:
        while game_close == True:
            window.fill(BLACK)
            Your_score(score)
            pygame.display.update()

            # Asking user to play again or quit
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # Validation of direction: avoid the overlap of snake's body
        if change_to == 'UP' and not direction == 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and not direction == 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and not direction == 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and not direction == 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        for enemy_snakes in enemy_snakes_snakes:
            if enemy_snakes['direction'] == 'UP':
                enemy_snakes['pos'][1] -= 10
            if enemy_snakes['direction'] == 'DOWN':
                enemy_snakes['pos'][1] += 10
            if enemy_snakes['direction'] == 'LEFT':
                enemy_snakes['pos'][0] -= 10
            if enemy_snakes['direction'] == 'RIGHT':
                enemy_snakes['pos'][0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            if invincible_time <= 0:
                score += 1
                framerate += 2
                food_spawn = False
                hunger += 50
                # Activate invincible state for 5 seconds (adjust the duration as needed)
                invincible_time = 0.3 * framerate
                # Check if it's time to add a new enemy snake
                new_enemy_snake = {
                    'pos': [400, 300],
                    'body': [[400, 300], [390, 300], [380, 300]],  # Initialize with an empty body
                    'directions': ['UP', 'DOWN', 'LEFT', 'RIGHT'],
                    'direction': random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT']),
                    'direction_change_interval': 5,  # Change direction every 5 frames
                    'direction_change_counter': 0
                }
                enemy_snakes_snakes.append(new_enemy_snake)
        else:
            snake_body.pop()

        # Decrement hunger over time
        hunger -= 0.3

        # Check if hunger reaches 0
        if hunger <= 0:
            game_close = True

        if hunger >= 100:
            hunger = 100

        # Enemy Snake body growing mechanism
        for enemy_snakes in enemy_snakes_snakes:
            enemy_snakes['body'].insert(0, list(enemy_snakes['pos']))
            if len(enemy_snakes['body']) > max_snake_length:
                enemy_snakes['body'].pop()
            if enemy_snakes['pos'][0] == food_pos[0] and enemy_snakes['pos'][1] == food_pos[1]:
                food_spawn = False
                # Add a new position to the enemy_snakes_body list
                enemy_snakes['body'].insert(0, list(enemy_snakes['pos']))

        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
            food_spawn = True

        # Limit the snake's length
        if len(snake_body) > max_snake_length:
            snake_body.pop()

        # Change enemy_snakes_direction periodically
        for enemy_snakes in enemy_snakes_snakes:
            enemy_snakes['direction_change_counter'] += 1
            if enemy_snakes['direction_change_counter'] >= enemy_snakes['direction_change_interval']:
                enemy_snakes['direction'] = random.choice(enemy_snakes['directions'])
                enemy_snakes['direction_change_counter'] = 0

        window.fill(BLACK)
        for pos in snake_body:
            pygame.draw.rect(window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        for enemy_snakes in enemy_snakes_snakes:
            for pos in enemy_snakes['body']:
                pygame.draw.rect(window, RED, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(window, YELLOW, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        if snake_pos[0] < 0 or snake_pos[0] > WIDTH - 10:
            game_close = True
        if snake_pos[1] < 0 or snake_pos[1] > HEIGHT - 10:
            game_close = True

        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_close = True

        # Check for collision with the enemy_snakes's body
        for enemy_snakes in enemy_snakes_snakes:
            for block in enemy_snakes['body']:
                if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                    if invincible_time <= 0:
                        game_close = True
            for block in snake_body:
                if (enemy_snakes['pos'][0] == block[0] and enemy_snakes['pos'][1] == block[1]):
                    # Check if the snake is not in the invincible state
                    if invincible_time <= 0:
                        game_close = True

        # Decrease invincible_time by 0.3 in each frame
        if invincible_time > 0:
            invincible_time -= 0.3

        # Enemy Snake collision with walls
        for enemy_snakes in enemy_snakes_snakes:
            if (enemy_snakes['pos'][0] < 0 or enemy_snakes['pos'][0] >= WIDTH or enemy_snakes['pos'][1] < 0 or enemy_snakes['pos'][1] >= HEIGHT):
                # Reset enemy_snakes snake's position and body
                enemy_snakes_snakes.remove(enemy_snakes)

        display_info(score, hunger)
        pygame.display.update()

        # Limit frame rate to 15 Hz
        pygame.time.Clock().tick(framerate)

    pygame.quit()
    quit()

# Run the game
gameLoop()
