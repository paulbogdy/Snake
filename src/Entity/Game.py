from src.Entity.Snake import Snake, Body
import random


class SnakeGame:
    def __init__(self, width, height, snake_dim):
        self.__width = width
        self.__height = height
        self.__score = 0
        self.__ended = False
        self.__apple = Body((random.randint(0, width // snake_dim - 1) * snake_dim,
                            random.randint(0, height / snake_dim - 1) * snake_dim),
                           (255, 0, 0), snake_dim)
        head = Body((int(width / snake_dim / 2 + 1) * snake_dim,
                     int(height / snake_dim / 2 + 1) * snake_dim),
                    (0, 0, 0), snake_dim)
        self.__snake = Snake(head, snake_dim)

    @property
    def food(self):
        return self.__apple

    @property
    def snake(self):
        return self.__snake.body

    @property
    def score(self):
        return self.__score

    @property
    def ended(self):
        return self.__ended

    def eat_apple(self):
        self.__score += 1
        self.__snake.eat()
        self.__apple = Body((random.randint(0, self.__width // self.__snake.dim - 1) * self.__snake.dim,
                             random.randint(0, self.__height / self.__snake.dim - 1) * self.__snake.dim),
                            (255, 0, 0), self.__snake.dim)

    def set_new_dir(self, new_dir):
        self.__snake.next_dir = new_dir

    def update(self):
        if self.__ended:
            return
        self.__snake.move()
        self.__snake.head.poz = (self.__snake.head.poz[0] % self.__width, self.__snake.head.poz[1] % self.__height)
        if self.__snake.head.poz == self.__apple.poz:
            self.eat_apple()
        if self.__snake.check_collision():
            self.__ended = True
