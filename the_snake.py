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

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты"""

    def __init__(self, body_color=None,
                 position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для будущей отрисовки змейки и яблока"""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко и его поведение"""

    def __init__(self, body_color=(255, 0, 0)):
        self.position = self.randomize_position()
        self.body_color = body_color

    def randomize_position(self) -> tuple:
        """Метод для генерации рандомных коодинат яблока"""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    # Метод draw класса Apple
    def draw(self) -> None:
        """Метод для отрисовки яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и ее поведение"""

    def __init__(self, length=1, last=None,
                 positions=[(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)],
                 direction=RIGHT, next_direction=None, body_color=(0, 255, 0)):
        super().__init__(body_color=body_color, position=positions[0])
        self.length = length
        self.last = last
        self.positions = positions
        self.direction = direction
        self.next_direction = next_direction
        self.body_color = body_color
        # super().__init__(position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self) -> None:
        """Метод для обновления направления змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    # Метод draw класса Snake
    def draw(self) -> None:
        """Метод для отрисовки змейки"""
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

    def get_head_position(self) -> tuple:
        """Метод, возвращающий координаты головы змейки"""
        return self.positions[0]

    def move(self):
        """Метод, описывающий движение змейки"""
        current_position = list(self.get_head_position())
        if self.direction == RIGHT:
            current_position[0] += GRID_SIZE
        elif self.direction == LEFT:
            current_position[0] -= GRID_SIZE
        elif self.direction == UP:
            current_position[1] -= GRID_SIZE
        elif self.direction == DOWN:
            current_position[1] += GRID_SIZE

        current_position[0] %= SCREEN_WIDTH
        current_position[1] %= SCREEN_HEIGHT

        if tuple(current_position) in self.positions[2:]:
            for position in self.positions:
                rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
            self.reset()
        else:
            self.positions.insert(0, tuple(current_position))
            if len(self.positions) > self.length:
                # Запоминаем последний сегмент перед удалением
                if len(self.positions) > self.length:
                    self.last = self.positions.pop()
                else:
                    self.last = None

    def reset(self) -> None:
        """Метод для возвращения змейки в начальное положение"""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """функция для описания действий пользователя"""
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


def check_apple_collision(snake, apple):
    """Функция для проверки столкновения головы змейки и яблока"""
    if snake.get_head_position() == apple.position:
        snake.length += 1
        while True:
            position = apple.randomize_position()
            if position not in snake.positions:
                apple.position = position
                break


def main():
    """Точка входа в программу, главный цикл"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        check_apple_collision(snake, apple)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
