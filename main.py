import pygame
from pygame.locals import *
import time
SIZE = 40
BACKGROUND_COLOR = (153, 255, 255)


class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        self.block = pygame.image.load("resource/snake_body.png")
        self.x = SIZE
        self.y = SIZE
        self.direction = 'down'

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        self.parent_screen.blit(self.block, (self.x, self.y))
        pygame.display.flip()

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def walk(self):

        if self.direction == 'up':
            self.y -= SIZE
        if self.direction == 'down':
            self.y += SIZE
        if self.direction == 'right':
            self.x += SIZE
        if self.direction == 'left':
            self.x -= SIZE
        self.draw()


class Game:
    def __init__(self):
        pygame.init()

        # this is the game window
        self.surface = pygame.display.set_mode((1200, 600))

        # change the screen color
        self.surface.fill(BACKGROUND_COLOR)

        self.snake = Snake(self.surface, 1)
        self.snake.draw()

    def run(self):
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        loop = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                elif event.type == QUIT:
                    loop = False
            self.snake.walk()
            time.sleep(0.3)

if __name__ == '__main__':
    game = Game()
    game.run()
