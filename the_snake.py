from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет апельсина
ORANGE_COLOR = (253, 165, 15)

# Цвет черники
BLUEBERRY_COLOR = (79, 135, 247)

# Цвет камня
STONE_COLOR = (173, 165, 135)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        self.position = (randint(1, 31) * GRID_SIZE,
                         randint(1, 23) * GRID_SIZE)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.length = 2
        self.positions = [self.position, ]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        # определение координаты по х:
        temporary_x_value = (
            self.positions[0][0] + self.direction[0] * GRID_SIZE
        )
        if temporary_x_value > SCREEN_WIDTH:
            temporary_x_value -= SCREEN_WIDTH
        if temporary_x_value < 0:
            temporary_x_value += SCREEN_WIDTH
        # определение координаты по у:
        temporary_y_value = (
            self.positions[0][1] + self.direction[1] * GRID_SIZE
        )
        if temporary_y_value > SCREEN_HEIGHT:
            temporary_y_value -= SCREEN_HEIGHT
        if temporary_y_value < 0:
            temporary_y_value += SCREEN_HEIGHT
        self.positions.insert(0, (temporary_x_value, temporary_y_value))
        if len(self.positions) > int(self.length):
            list.pop(self.positions)

    # Метод draw класса Snake
    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    # не понимаю, для чего нужен метод ;(
    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        self.length = 2
        self.positions.clear()
        self.positions = [self.position, ]
        directions = (UP, DOWN, LEFT, RIGHT)
        self.direction = choice(directions)


class Bluererry(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = BLUEBERRY_COLOR

    def randomize_position(self):
        self.position = (randint(1, 31) * GRID_SIZE,
                         randint(1, 23) * GRID_SIZE)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Stone(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = STONE_COLOR

    def randomize_position(self):
        self.position = (randint(1, 31) * GRID_SIZE,
                         randint(1, 23) * GRID_SIZE)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def upgrade(self, length):
        if length == 5 or length == 9:
            return True
        else:
            return False


class Orange(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = ORANGE_COLOR

    def randomize_position(self):
        self.position = (randint(1, 31) * GRID_SIZE,
                         randint(1, 23) * GRID_SIZE)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def upgrade(self, length):
        if length == 3 or length == 7:
            return True
        else:
            return False


# Функция обработки действий пользователя
def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    # Инициализация PyGame:
    pygame.init()
    # поздаем переменную от константы для изменения скорости от апельсинки
    speed = SPEED
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    apple.randomize_position()
    snake = Snake()
    orange = Orange()
    orange.randomize_position()
    bluererry = Bluererry()
    bluererry.randomize_position()
    stone = Stone()
    stone.randomize_position()
    while True:
        clock.tick(speed)
        apple.draw()
        bluererry.draw()
        snake.draw()
        snake.move()
        snake.update_direction()
        handle_keys(snake)
        # событие - условие появления апельсинки
        if orange.upgrade(snake.length):
            orange.draw()
        # событие - змейка съела апельсинку
        if orange.position == snake.positions[0]:
            speed += 10
            snake.length += 1
            orange.randomize_position()
        # событие - змейка съела яблоко
        if apple.position == snake.positions[0]:
            snake.length += 1
            apple.randomize_position()
        # событие - змейка съела чернику
        if bluererry.position == snake.positions[0]:
            if snake.length > 2:
                snake.length -= 1
            bluererry.randomize_position()
        # событие - условие появления камня
        if stone.upgrade(snake.length):
            stone.draw()
        # событие - змейка съела камень
        if stone.position == snake.positions[0]:
            snake.reset()
        # событие - змейка съела себя:
        if len(snake.positions) >= 3:
            for i in range(1, len(snake.positions) - 1):
                if snake.positions[i] == snake.positions[0]:
                    snake.reset()
        pygame.display.update()
        screen.fill(BOARD_BACKGROUND_COLOR)


if __name__ == '__main__':
    main()
