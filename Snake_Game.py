

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
BLUE = (0, 0, 255)

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

# Maximum snake length
max_snake_length = 10  # Adjust this value as needed

# Competitor1 Snake properties
competitor1_pos = [320, 300]
competitor1_body = [[320, 300], [320, 310], [320, 320]]
competitor1_directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
competitor1_direction = random.choice(competitor1_directions)
competitor1_direction_change_interval = 5  # Change direction every 20 frames
competitor1_direction_change_counter = 0

competitor2_pos = [320, 300]
competitor2_body = [[320, 300], [320, 310], [320, 320]]
competitor2_directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
competitor2_direction = random.choice(competitor2_directions)
competitor2_direction_change_interval = 5  # Change direction every 20 frames
competitor2_direction_change_counter = 0


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
    global competitor1_pos, competitor1_body, competitor1_direction
    global competitor2_pos, competitor2_body, competitor2_direction
    global competitor1_direction_change_counter, competitor2_direction_change_counter

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

        # Moving the competitor1 snake
        if competitor1_direction == 'UP':
            competitor1_pos[1] -= 10
        if competitor1_direction == 'DOWN':
            competitor1_pos[1] += 10
        if competitor1_direction == 'LEFT':
            competitor1_pos[0] -= 10
        if competitor1_direction == 'RIGHT':
            competitor1_pos[0] += 10

        if competitor2_direction == 'UP':
            competitor2_pos[1] -= 10
        if competitor2_direction == 'DOWN':
            competitor2_pos[1] += 10
        if competitor2_direction == 'LEFT':
            competitor2_pos[0] -= 10
        if competitor2_direction == 'RIGHT':
            competitor2_pos[0] += 10

        # Snake body growing mechanism: insert a new position (snake_pose) on
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            framerate += 2
            food_spawn = False
            hunger += 10
        else:
            snake_body.pop()

        if hunger >= 100:
            hunger = 100

        # Decrement hunger over time
        hunger -= 0.1

        # Check if hunger reaches 0
        if hunger <= 0:
            game_close = True

        # Competitor1 Snake body growing mechanism
        competitor1_body.insert(0, list(competitor1_pos))
        if len(competitor1_body) > max_snake_length:
            competitor1_body.pop()
        if competitor1_pos[0] == food_pos[0] and competitor1_pos[1] == food_pos[1]:
            food_spawn = False
            # Add a new position to the competitor1_body list
            competitor1_body.insert(0, list(competitor1_pos))

        competitor2_body.insert(0, list(competitor2_pos))
        if len(competitor2_body) > max_snake_length:
            competitor2_body.pop()
        if competitor2_pos[0] == food_pos[0] and competitor2_pos[1] == food_pos[1]:
            food_spawn = False
            # Add a new position to the competitor1_body list
            competitor2_body.insert(0, list(competitor2_pos))

        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
            food_spawn = True

        # Limit the snake's length
        if len(snake_body) > max_snake_length:
            snake_body.pop()

        # Change competitor1_direction periodically
        competitor1_direction_change_counter += 1
        if competitor1_direction_change_counter >= competitor1_direction_change_interval:
            competitor1_direction = random.choice(competitor1_directions)
            competitor1_direction_change_counter = 0

        competitor2_direction_change_counter += 1
        if competitor2_direction_change_counter >= competitor2_direction_change_interval:
            competitor2_direction = random.choice(competitor2_directions)
            competitor2_direction_change_counter = 0

        window.fill(BLACK)
        for pos in snake_body:
            pygame.draw.rect(window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        for pos in competitor1_body:
            pygame.draw.rect(window, RED, pygame.Rect(pos[0], pos[1], 10, 10))

        for pos in competitor2_body:
            pygame.draw.rect(window, RED, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(window, BLUE, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        if snake_pos[0] < 0 or snake_pos[0] > WIDTH - 10:
            game_close = True
        if snake_pos[1] < 0 or snake_pos[1] > HEIGHT - 10:
            game_close = True

        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_close = True

        # Check for collision with the competitor1's body
        for block in competitor1_body:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_close = True

        for block in competitor2_body:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_close = True

        for block in snake_body:
            if (competitor1_pos[0] == block[0] and competitor1_pos[1] == block[1]) or (competitor2_pos[0] == block[0] and competitor2_pos[1] == block[1]):
                game_close = True

        # Inside the game loop
        # Competitor1 Snake collision with walls
        if (competitor1_pos[0] < 0 or competitor1_pos[0] >= WIDTH or competitor1_pos[1] < 0 or competitor1_pos[1] >= HEIGHT):
            # Reset competitor1 snake's position and body
            competitor1_pos = [320, 300]
            competitor1_body = [[320, 300], [320, 310], [320, 320]]
            competitor1_direction = random.choice(competitor1_directions)

        if (competitor2_pos[0] < 0 or competitor2_pos[0] >= WIDTH or competitor2_pos[1] < 0 or competitor2_pos[1] >= HEIGHT):
            # Reset competitor1 snake's position and body
            competitor2_pos = [320, 300]
            competitor2_body = [[320, 300], [320, 310], [320, 320]]
            competitor2_direction = random.choice(competitor2_directions)

        display_info(score, hunger)
        pygame.display.update()

        # Limit frame rate to 15 Hz
        pygame.time.Clock().tick(framerate)

    pygame.quit()
    quit()

# Run the game
gameLoop()
