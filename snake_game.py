import pygame
import time
import random
import sys

# Initialize pygame
pygame.init()

# Game Settings
WINDOW_X, WINDOW_Y = 720, 480
BLOCK_SIZE = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

# Game Window
game_window = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
pygame.display.set_caption("🐍 Dynamic Difficulty Snake Game")

# Clock
clock = pygame.time.Clock()

# Fonts
def get_font(size):
    return pygame.font.SysFont('times new roman', size)

# Score display
def show_score(score, level):
    font = get_font(20)
    score_surface = font.render(f'Score: {score}  |  Level: {level}', True, WHITE)
    game_window.blit(score_surface, (10, 10))

# Game over screen
def game_over_screen(score):
    game_window.fill(BLACK)
    game_over_text = get_font(50).render(f'Game Over!', True, RED)
    score_text = get_font(30).render(f'Your Score: {score}', True, WHITE)
    replay_text = get_font(20).render('Press R to Replay or Q to Quit', True, GREEN)

    game_window.blit(game_over_text, game_over_text.get_rect(center=(WINDOW_X/2, WINDOW_Y/4)))
    game_window.blit(score_text, score_text.get_rect(center=(WINDOW_X/2, WINDOW_Y/2)))
    game_window.blit(replay_text, replay_text.get_rect(center=(WINDOW_X/2, WINDOW_Y*3/4)))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Main Game Function
def main():
    # Initial snake and fruit settings
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    fruit_pos = [random.randrange(1, WINDOW_X//BLOCK_SIZE) * BLOCK_SIZE,
                 random.randrange(1, WINDOW_Y//BLOCK_SIZE) * BLOCK_SIZE]
    fruit_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0
    paused = False

    # Dynamic difficulty
    base_speed = 10
    level = 1

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'
                elif event.key == pygame.K_p:
                    paused = not paused

        if paused:
            continue

        direction = change_to

        # Move snake
        if direction == 'UP':
            snake_pos[1] -= BLOCK_SIZE
        elif direction == 'DOWN':
            snake_pos[1] += BLOCK_SIZE
        elif direction == 'LEFT':
            snake_pos[0] -= BLOCK_SIZE
        elif direction == 'RIGHT':
            snake_pos[0] += BLOCK_SIZE

        # Grow snake
        snake_body.insert(0, list(snake_pos))
        if snake_pos == fruit_pos:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        # Increase difficulty every 50 points
        level = score // 50 + 1
        speed = base_speed + (level - 1) * 2

        # Spawn fruit
        if not fruit_spawn:
            fruit_pos = [random.randrange(1, WINDOW_X//BLOCK_SIZE) * BLOCK_SIZE,
                         random.randrange(1, WINDOW_Y//BLOCK_SIZE) * BLOCK_SIZE]
            fruit_spawn = True

        # Game Over conditions
        if (snake_pos[0] < 0 or snake_pos[0] >= WINDOW_X or
            snake_pos[1] < 0 or snake_pos[1] >= WINDOW_Y):
            break
        for block in snake_body[1:]:
            if snake_pos == block:
                break
        else:
            # Draw everything
            game_window.fill(BLACK)
            for pos in snake_body:
                pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(game_window, WHITE, pygame.Rect(fruit_pos[0], fruit_pos[1], BLOCK_SIZE, BLOCK_SIZE))
            show_score(score, level)
            pygame.display.update()
            clock.tick(speed)
            continue

        break

    game_over_screen(score)

# Run game
if __name__ == "__main__":
    main()