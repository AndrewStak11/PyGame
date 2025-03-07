import pygame
from random import randrange
import sys

# Константы
RES = 800
SIZE = 50

# Функция для сброса игры
def reset_game():
    global x, y, apple, dirs, length, snake, dx, dy, score, fps
    x, y = SIZE, SIZE  # Начальная позиция
    apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
    dirs = {'W': True, 'S': True, 'A': True, 'D': True}
    length = 1
    snake = [(x, y)]
    dx, dy = 1, 0  # Начальное движение вправо
    score = 0
    fps = 5  # Уменьшено с 10 до 5

# Начальные параметры змейки и яблока
x, y = SIZE, SIZE
apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
dirs = {'W': True, 'S': True, 'A': True, 'D': True}
length = 1
snake = [(x, y)]
dx, dy = 1, 0
score = 0
fps = 5  # Уменьшено с 10 до 5

# Инициализация Pygame
pygame.init()
sc = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()
font_score = pygame.font.SysFont('Arial', 26, bold=True)
font_end = pygame.font.SysFont('Arial', 66, bold=True)
font_restart = pygame.font.SysFont('Arial', 36, bold=True)

# Загрузка изображения фона
try:
    img = pygame.image.load('images/snake.png').convert()
    img = pygame.transform.scale(img, (RES, RES))
except FileNotFoundError:
    print("Ошибка: Файл images/snake.png не найден. Использую зелёный фон.")
    img = pygame.Surface((RES, RES))
    img.fill((0, 255, 0))

# Основной цикл
running = True
game_over = False
while running:
    if not game_over:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and dirs['W']:
            dx, dy = 0, -1
            dirs = {'W': True, 'S': False, 'A': True, 'D': True}
        if keys[pygame.K_s] and dirs['S']:
            dx, dy = 0, 1
            dirs = {'W': False, 'S': True, 'A': True, 'D': True}
        if keys[pygame.K_a] and dirs['A']:
            dx, dy = -1, 0
            dirs = {'W': True, 'S': True, 'A': True, 'D': False}
        if keys[pygame.K_d] and dirs['D']:
            dx, dy = 1, 0
            dirs = {'W': True, 'S': True, 'A': False, 'D': True}

        # Отрисовка фона
        sc.blit(img, (0, 0))

        # Отрисовка змейки и яблока
        [pygame.draw.rect(sc, pygame.Color('green'), (i, j, SIZE - 2, SIZE - 2)) for i, j in snake]
        pygame.draw.rect(sc, pygame.Color('red'), (*apple, SIZE, SIZE))

        # Отрисовка счёта
        render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('orange'))
        sc.blit(render_score, (5, 5))

        # Движение змейки
        x += dx * SIZE
        y += dy * SIZE
        snake.append((x, y))
        snake = snake[-length:]

        # Поедание яблока
        if snake[-1] == apple:
            apple = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
            length += 1
            score += 1
            fps += 0.5  # Уменьшен прирост скорости с 1 до 0.5

        # Проверка на столкновение с границами или собой
        if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
            game_over = True

        # Обновление экрана
        pygame.display.flip()
        clock.tick(fps)

    else:
        # Экран "GAME OVER"
        sc.blit(img, (0, 0))
        render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
        render_restart = font_restart.render('Press R to Restart', 1, pygame.Color('white'))
        sc.blit(render_end, (RES // 2 - 200, RES // 3))
        sc.blit(render_restart, (RES // 2 - 150, RES // 2))
        pygame.display.flip()

        # Обработка событий на экране "GAME OVER"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    game_over = False

# Завершение программы
pygame.quit()
sys.exit()