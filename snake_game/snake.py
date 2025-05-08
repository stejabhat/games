import pygame
import time
import random
import os

# Initialize
pygame.init()

# Display settings
width, height = 600, 400
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game with Scorecard')

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
gray = (170, 170, 170)

# Game settings
snake_block = 10
snake_speed = 15
clock = pygame.time.Clock()
font = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 30)

# High score file
highscore_file = "highscore.txt"
if not os.path.exists(highscore_file):
    with open(highscore_file, "w") as f:
        f.write("0")

def get_high_score():
    with open(highscore_file, "r") as f:
        return int(f.read())

def update_high_score(score):
    high_score = get_high_score()
    if score > high_score:
        with open(highscore_file, "w") as f:
            f.write(str(score))

def draw_text(msg, color, x, y, size=25):
    font_local = pygame.font.SysFont("bahnschrift", size)
    mesg = font_local.render(msg, True, color)
    dis.blit(mesg, [x, y])

def your_score(score, high_score):
    score_text = score_font.render(f"Score: {score}  High Score: {high_score}", True, yellow)
    dis.blit(score_text, [10, 10])

def draw_snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], block, block])

def game_loop():
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            dis.fill(blue)
            final_score = length_of_snake - 1
            high_score = get_high_score()
            update_high_score(final_score)

            draw_text("Game Over!", red, width / 3, height / 4, size=40)
            draw_text("Click Restart or press Q to Quit", white, width / 4.5, height / 2.5)

            your_score(final_score, high_score)
            pygame.draw.rect(dis, gray, [width / 2.5, height / 1.8, 100, 40])
            draw_text("Restart", black, width / 2.5 + 10, height / 1.8 + 5)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if width / 2.5 <= mx <= width / 2.5 + 100 and height / 1.8 <= my <= height / 1.8 + 40:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Border collision
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Self collision
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list)
        your_score(length_of_snake - 1, get_high_score())

        pygame.display.update()

        # Food collision
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()
