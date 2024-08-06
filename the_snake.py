from random import choice, randrange

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

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

ORANGE_COLOR = (253, 165, 15)

BLUEBERRY_COLOR = (79, 135, 247)

STONE_COLOR = (173, 165, 135)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject():
    """Описание начального класса"""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Метод прорисовки для объекта"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Метод определения случайного положения объекта"""
        self.position = (randrange(20, 620, 20),
                         randrange(20, 460, 20))


class Apple(GameObject):
    """Описание класса для яблока"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR


class Snake(GameObject):
    """Определение для класса змеи"""

    def __init__(self):
        super().__init__()
        self.length = 2
        self.positions = [self.position, ]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, описывающий движение змейки"""
        # # определение координаты по х:
        temporary_x_value = (
            self.positions[0][0] + self.direction[0] * GRID_SIZE
        )
        # определение координаты по у:
        temporary_y_value = (
            self.positions[0][1] + self.direction[1] * GRID_SIZE
        )
        self.positions.insert(0, (temporary_x_value % SCREEN_WIDTH,
                                  temporary_y_value % SCREEN_HEIGHT))
        if len(self.positions) > int(self.length):
            list.pop(self.positions)

    # Метод draw - переобределение для класса Snake
    def draw(self):
        """Метод прорисовки для объекта"""
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

    # не понимаю, для чего нужно использовать метод, обошелся без него ;(
    def get_head_position(self):
        """Не использовался"""
        return self.positions[0]

    def reset(self):
        """Метод для возвращения к начальным параметрам"""
        self.length = 2
        self.positions = [self.position, ]
        directions = (UP, DOWN, LEFT, RIGHT)
        self.direction = choice(directions)


class Bluererry(GameObject):
    """Описание класса для черники"""

    def __init__(self):
        super().__init__()
        self.body_color = BLUEBERRY_COLOR


class Stone(GameObject):
    """Описание класса для камня"""

    def __init__(self):
        super().__init__()
        self.body_color = STONE_COLOR

    def upgrade(self, length):
        """Метод определения условия появления камня"""
        return length == 5 or length == 9


class Orange(GameObject):
    """Описание класса для апельсина"""

    def __init__(self):
        super().__init__()
        self.body_color = ORANGE_COLOR

    def upgrade(self, length):
        """Метод определения условия появления апельсина"""
        return length == 3 or length == 7


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
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


apple = Apple()
apple.randomize_position()
snake = Snake()
orange = Orange()
orange.randomize_position()
bluererry = Bluererry()
bluererry.randomize_position()
stone = Stone()
stone.randomize_position()


def snake_eating_itself():
    """событие - змейка скушала себя"""
    for i in range(1, len(snake.positions) - 1):
        if snake.positions[i] == snake.positions[0]:
            snake.reset()


def main():
    """Главная функция"""
    # Инициализация PyGame:
    pygame.init()
    # cоздаем переменную от константы для изменения скорости от апельсинки
    speed = SPEED
    # запускаем цикл игры
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
            speed = SPEED
        # событие - змейка съела себя:
        if len(snake.positions) >= 3:
            snake_eating_itself
            speed = SPEED

        pygame.display.update()
        screen.fill(BOARD_BACKGROUND_COLOR)


if __name__ == '__main__':
    main()
