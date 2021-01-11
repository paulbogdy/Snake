import pygame
from src.Entity.Game import SnakeGame
import os


class Text:
    def __init__(self, position, txt="", font=None, size=32, color=(255, 255, 255)):
        font = pygame.font.SysFont(font, size)
        self.__pos = position
        self.__img = font.render(txt, True, color)

    def draw(self, screen, aux_pos=(0, 0)):
        screen.blit(self.__img, (aux_pos[0] + self.__pos[0], aux_pos[1] + self.__pos[1]))


class Button:
    def __init__(self, width, height, position, action=None, color=(0, 0, 0), text=None):
        self.__width = width
        self.__height = height
        self.__position = position
        self.__action = action
        self.__color = color
        self.__text = text

    @property
    def pos(self):
        return self.__position

    def draw(self, screen):
        pygame.draw.rect(screen, self.__color, (self.__position[0], self.__position[1], self.__width, self.__height))
        if self.__text is not None:
            self.__text.draw(screen, self.__position)

    def check_hit(self, pos):
        return self.__position[0] <= pos[0] <= self.__position[0] + self.__width and\
               self.__position[1] <= pos[1] <= self.__position[1] + self.__height

    def clicked(self):
        self.__action()


class GUI:
    def __init__(self):
        pygame.init()
        self.__width = 656
        self.__height = 656
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        self.__high_score = 0
        self.load_score()

    def load_score(self):
        if not os.path.exists("hs.txt"):
            file = open("hs.txt", "w")
            file.close()
            return
        f = open("hs.txt", "r")
        try:
            self.__high_score = int(f.read())
        except:
            pass
        f.close()

    def save_score(self):
        f = open("hs.txt", "w")
        f.write(str(self.__high_score))
        f.close()

    def run(self):
        running = True
        buttons = []
        btn_text = Text((40, 10), txt="Start", font='Corbel', size=35)
        buttons.append(Button(150, 50, (253, 303), self.run_snake, text=btn_text))
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    for button in buttons:
                        if button.check_hit(mouse):
                            button.clicked()
            hs_text = Text((200, 50), txt="High Score: " + str(self.__high_score),
                                font='Corbel', size=50, color=(0, 0, 0))
            self.__screen.fill((255, 255, 255))
            hs_text.draw(self.__screen)
            for button in buttons:
                button.draw(self.__screen)
            pygame.display.update()

    def draw(self, body):
        pygame.draw.rect(self.__screen, body.color, (body.poz[0], body.poz[1], body.dim, body.dim))

    def run_snake(self):
        clock = pygame.time.Clock()
        game = SnakeGame(self.__width, self.__height, 16)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        game.set_new_dir((-1, 0))
                    elif event.key == pygame.K_UP:
                        game.set_new_dir((0, -1))
                    elif event.key == pygame.K_RIGHT:
                        game.set_new_dir((1, 0))
                    elif event.key == pygame.K_DOWN:
                        game.set_new_dir((0, 1))
            game.update()
            if game.ended:
                self.__high_score = max(self.__high_score, game.score)
                self.save_score()
                running = False
            self.__screen.fill((255, 255, 255))
            food = game.food
            self.draw(food)
            snake = game.snake
            for body in reversed(snake):
                self.draw(body)
            pygame.display.update()
            clock.tick(60)

