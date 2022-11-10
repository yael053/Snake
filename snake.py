import pygame
import random


pygame.font.init()

MAT_WIDTH, MAT_HEIGHT = 20, 20
SQUARE_SIZE = 30
WIDTH, HEIGHT = MAT_WIDTH * SQUARE_SIZE, MAT_HEIGHT * SQUARE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("snake Game")

clock = pygame.time.Clock()
FPS = 60
MOVE_TIME = 500
TURRET_MIN_TIME = 10000
TURRET_MAX_TIME = 25000

shoot_val = 7

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)



COLORS = {'PURPLE': (166, 45, 151),
          'LIGHT_BLUE': (0, 128, 255),
          'ORANGE': (255, 128, 0),
          'GREEN': (0, 255, 0),
          'YELLOW': (255, 255, 0)}

SNAKE_HEAD_ROUND = 15
SNAKE_BODY_ROUND = 5
APPLE_ROUND = 10

SNAKE_ROUND_DICT = {
    "left": [0, 1, 0, 1],
    "right": [1, 0, 1, 0],
    "up": [0, 1, 1, 0],
    "down": [1, 0, 0, 1]
}


def draw_screen(snake_rects, snake_color, apples_rects, apple_color, bom_apples_rect, direction):
    screen.fill(BLACK)
    for rect in apples_rects:
        pygame.draw.rect(screen, apple_color, rect, 0, *[APPLE_ROUND for _ in range(4)])

    for rect in bom_apples_rect:
        pygame.draw.rect(screen, apple_color, rect, 0, *[APPLE_ROUND for _ in range(4)])

    pygame.draw.rect(screen, snake_color, snake_rects[0], 0,
                     *[SNAKE_HEAD_ROUND if corner else SNAKE_BODY_ROUND for corner in SNAKE_ROUND_DICT[direction]])
    for rect in snake_rects[1:]:
        pygame.draw.rect(screen, snake_color, rect, 0, *[SNAKE_BODY_ROUND for _ in range(4)])
    border_rects = create_border_rects()


    for rect in border_rects:
        pygame.draw.rect(screen, WHITE, rect, 0, *[SNAKE_BODY_ROUND for _ in range(4)])

    pygame.display.update()


def get_direction(direction):
    for event in pygame.event.get():
        event_dict = event.__dict__
        if 'unicode' not in event_dict:
            continue
        button_pressed = event_dict['unicode']
        if button_pressed.lower() == 'w' and direction != "down":
            return "up"

        if button_pressed.lower() == 'd' and direction != "left":
            return "right"

        if button_pressed.lower() == 'a' and direction != "right":
            return "left"

        if button_pressed.lower() == 's' and direction != "up":
            return "down"

    return None


def move_snake(snake, apples, direction):
    head_x = snake[0][0]
    head_y = snake[0][1]

    if not handle_snake_eat_apple(snake, apples):
        snake.pop()

    if direction == "up":
        snake.insert(0, [head_x, head_y - 1])  # which index in the list, spot in the game

    elif direction == "right":
        snake.insert(0, [head_x + 1, head_y])

    elif direction == "left":
        snake.insert(0, [head_x - 1, head_y])

    elif direction == "down":
        snake.insert(0, [head_x, head_y + 1])


def handle_snake_eat_apple(snake, apples):
    for i, apple in enumerate(apples):
        if snake[0][0] == apple[0] and snake[0][1] == apple[1]:
            apples.pop(i)
            return True
    return False


def is_snake_eat_apple(snake, apples):
    for i, apple in enumerate(apples):
        if snake[0][0] == apple[0] and snake[0][1] == apple[1]:
            return True
    return False


def is_alive(snake, bomb_apples):
    alive = True

    if snake[0][0] == 0 or snake[0][0] == MAT_WIDTH - 1 or snake[0][1] == 0 or snake[0][1] == MAT_HEIGHT - 1:
        alive = False

    for snake_body in snake[1:]:
        if snake[0][0] == snake_body[0] and snake[0][1] == snake_body[1]:
            alive = False

    for apple in bomb_apples:
        if snake[0][0] == apple[0] and snake[0][1] == apple[1]:
            alive = False

    return alive


def create_border_rects():
    border = []
    for i in range(MAT_HEIGHT):
        border.append([0, i])  # col
        border.append([MAT_WIDTH - 1, i])
    for i in range(MAT_WIDTH):
        border.append([i, 0])  # row
        border.append([i, MAT_HEIGHT - 1])
    # border = set(border)

    border_rects = []
    for x, y in border:
        border_rects.append(create_rect(x, y))
    return border_rects


def find_empty_square(snake=[], apples=[], bomb_apples=[]):
    if bomb_apples is None:
        bomb_apples = []
    taken_squares = snake + apples + bomb_apples
    new_square = [random.randint(1, MAT_WIDTH - 2), random.randint(1, MAT_HEIGHT - 2)]
    is_taken = True

    while is_taken:
        new_square = [random.randint(1, MAT_WIDTH - 2), random.randint(1, MAT_HEIGHT - 2)]
        is_taken = False
        for sqr in taken_squares:
            if new_square[0] == sqr[0] and new_square[1] == sqr[1]:
                is_taken = True
                break

    return new_square


def generate_new_apples(apple_count, snake, apples, bomb_apples):
    for i in range(apple_count):
        apples.append(find_empty_square(snake, apples, bomb_apples))


def create_rect(mat_x, mat_y):
    return pygame.Rect(mat_x * SQUARE_SIZE + 1, mat_y * SQUARE_SIZE + 1, SQUARE_SIZE - 4, SQUARE_SIZE - 4)


def main():
    snake = [find_empty_square()]  # python
    apples = [find_empty_square(snake)]
    bomb_apples = [find_empty_square(snake, apples)]

    prev_move_time = 0
    prev_move = "left"
    new_move = "left"

    snake_color = COLORS["LIGHT_BLUE"]
    apple_color = COLORS["GREEN"]

    while is_alive(snake, bomb_apples):
        clock.tick(FPS)

        curr_time = pygame.time.get_ticks()
        if curr_time - prev_move_time < MOVE_TIME:
            check_direction = get_direction(prev_move)

            if check_direction:
                new_move = check_direction
            continue
        prev_move_time = curr_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if len(apples) == 0:
            generate_new_apples(2, snake, apples, bomb_apples)
            bomb_apples = [find_empty_square(snake, apples)]
            snake_color = apple_color
            apple_color = random.choice(list(COLORS.values()))
            while apple_color == snake_color:
                apple_color = random.choice(list(COLORS.values()))

        snake_rects = []
        for x, y in snake:
            snake_rects.append(create_rect(x, y))  # draw

        apples_rects = []
        for x, y in apples:
            apples_rects.append(create_rect(x, y))  # draw

        bomb_apples_rect = []
        for x, y in bomb_apples:
            bomb_apples_rect.append(create_rect(x, y))

        move_snake(snake, apples, new_move)
        draw_screen(snake_rects, snake_color, apples_rects, apple_color, bomb_apples_rect, prev_move)
        prev_move = new_move
    snake_color = RED
    draw_screen(snake_rects, snake_color, apples_rects, apple_color, bomb_apples_rect, prev_move)
    pygame.time.delay(2000)

    pygame.display.update()
    main()


if __name__ == "__main__":
    main()
