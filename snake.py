import pygame
import random


#---Options---------------------------------
RESOLUTION = 800,800
SCALABLE = True
DEFAULT_SPEED = 15
CELL = 40
#-------------------------------------------


SNAKE = []
FOOD = None
changed_direction = False
GAME = "Waiting"
direction = None
POINTS = 0
SPEED = DEFAULT_SPEED

def start_game():
    print("STARTING GAME")
    global GAME
    GAME = "Running"
    SNAKE.append([(RESOLUTION[0] // CELL) // 2, (RESOLUTION[1] // CELL) // 2])
    generate_food()

def convert_coords(coords):
    max_y = RESOLUTION[1] // CELL
    x, y = coords
    return x, max_y - y - 1

def draw_snake():
    for cell in SNAKE:
        x, y = convert_coords(cell)
        pygame.draw.rect(screen, "green", (x * CELL, y * CELL, CELL, CELL))

def change_direction(new_direction):
    print("Changing direction", new_direction)
    global direction
    global changed_direction
    if not changed_direction:
        if new_direction == "left" and direction != "right":
            direction = new_direction
        elif new_direction == "right" and direction != "left":
            direction = new_direction
        elif new_direction == "up" and direction != "down":
            direction = new_direction
        elif new_direction == "down" and direction != "up":
            direction = new_direction
        changed_direction = True

def move_snake():
    global GAME
    if GAME == "Running":
        directions = {"up": (0, 1), "down": (0, -1), "left": (-1, 0), "right": (1, 0)}
        global direction
        global FOOD
        global POINTS
        SNAKE.insert(0, list((SNAKE[0][0] + directions[direction][0], SNAKE[0][1] + directions[direction][1])))
        if SNAKE[0] == FOOD:
            FOOD = None
            POINTS += 1
            generate_food()
        else:
            if len(SNAKE) != 1:
                SNAKE.remove(SNAKE[len(SNAKE) - 1])
        if SNAKE[0] in SNAKE[1:]:
            end_game()
        elif SNAKE[0][0] < 0 or SNAKE[0][0] >= RESOLUTION[0] // CELL or SNAKE[0][1] < 0 or SNAKE[0][1] >= RESOLUTION[1] // CELL:
            end_game()
        draw_snake()

def generate_food():
    global FOOD
    global SPEED
    if GAME == "Running":
        if FOOD == None:
            FOOD = [random.randint(0, RESOLUTION[0] // CELL - 1),random.randint(0, RESOLUTION[0] // CELL - 1)]
            x, y = convert_coords(FOOD)
            pygame.draw.rect(screen, "yellow", (x * CELL, y * CELL, CELL, CELL))
            if (random.randint(0,100) < 10):
                SPEED += 1

def show_food():
    if FOOD != None:
        x, y = convert_coords(FOOD)
        pygame.draw.rect(screen, "yellow", (x * CELL, y * CELL, CELL, CELL))

def show_score():
    font = pygame.font.Font(None, 40)
    text = font.render(f"Score: {POINTS}", True, "white")
    screen.blit(text, (0, 0))

def end_game():
    global GAME
    global SNAKE
    global POINTS
    global SPEED
    draw_ending()
    GAME = "Ended"
    SNAKE = []
    POINTS = 0
    SPEED = 15

def draw_ending():
    font = pygame.font.Font(None, 50)
    text = font.render(f"GAME OVER! Score: {POINTS}", True, "red")
    screen.blit(text, (RESOLUTION[0] // 2 - (RESOLUTION[0] // 4), RESOLUTION[1] // 2))

pygame.init()
pygame.display.set_caption("Snake")
screen = pygame.display.set_mode((RESOLUTION))
clock = pygame.time.Clock()
screen.fill("black")
running = True
ticks = 0
time = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if GAME != "Ended":
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_w:
                    change_direction("up")
                elif event.key == pygame.K_s:
                    change_direction("down")
                elif event.key == pygame.K_a:
                    change_direction("left")
                elif event.key == pygame.K_d:
                    change_direction("right")
                if GAME == "Waiting":
                    start_game()
    if GAME == "Running":
        screen.fill("black")
        move_snake()
        show_food()
        show_score()
    elif GAME == "Ended":
        time += 1
        if time > SPEED:
            GAME = "Waiting"
            time = 0
    changed_direction = False
    pygame.display.update()
    pygame.display
    clock.tick(SPEED)
pygame.quit()