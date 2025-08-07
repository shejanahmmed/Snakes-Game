import pygame
import random
import os

pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 200, 0)

# Screen dimensions
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SnakesWithShejan")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# Text display function
def text_screen(text, color, x, y, center=False):
    screen_text = font.render(text, True, color)
    if center:
        text_rect = screen_text.get_rect(center=(x, y))
        gameWindow.blit(screen_text, text_rect)
    else:
        gameWindow.blit(screen_text, [x, y])

# Draw the snake
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# Welcome screen function
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        text_screen("🐍 Welcome to SnakesWithShejan 🐍", black, screen_width / 2, screen_height / 3, center=True)
        text_screen("Press SPACE BAR to Play", green, screen_width / 2, screen_height / 2, center=True)
        text_screen("Press ESC to Exit", red, screen_width / 2, screen_height / 2 + 60, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()
                elif event.key == pygame.K_ESCAPE:
                    exit_game = True

        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    quit()

# Main game function
def gameloop():
    # Ensure high score file exists
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    hiscore = int(hiscore.strip()) if hiscore.strip().isdigit() else 0

    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5

    food_x = random.randint(20, screen_width - 20)
    food_y = random.randint(20, screen_height - 20)

    score = 0
    snake_size = 10
    fps = 30
    snk_list = []
    snk_length = 1

    while not exit_game:
        if game_over:
            gameWindow.fill(white)
            text_screen("Game Over! Press Enter To Continue.", red, screen_width / 2, screen_height / 2, center=True)
            text_screen(f"Your Score: {score * 10}", black, screen_width / 2, screen_height / 2 + 50, center=True)
            text_screen(f"High Score: {hiscore * 10}", black, screen_width / 2, screen_height / 2 + 100, center=True)

            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()
                        return
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    elif event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    #Enjoy your cheatcode
                    elif event.key == pygame.K_q:
                        score +=5

            snake_x += velocity_x
            snake_y += velocity_y

            # Eating food
            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                score += 1
                food_x = random.randint(20, screen_width - 20)
                food_y = random.randint(20, screen_height - 20)
                snk_length += 5
                if score > hiscore:
                    hiscore = score

            gameWindow.fill(white)
            text_screen("Score : " + str(score * 10), red, 5, 5)
            text_screen("High Score : " + str(hiscore * 10), black, 600, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = [snake_x, snake_y]
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            # Self collision
            if head in snk_list[:-1]:
                game_over = True

            # Wall collision
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            plot_snake(gameWindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

# Start with welcome screen
welcome()
