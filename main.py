import pygame
from pygame.locals import *

SIZE = 40
BACKGROUND_COLOR = (153, 255, 255)


class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        self.block = pygame.image.load("resource/snake_body.png")
        self.x = SIZE
        self.y = SIZE

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        self.parent_screen.blit(self.block, (self.x, self.y))
        pygame.display.flip()

    def move_left(self):
        self.x -= 10
        self.draw()

    def move_right(self):
        self.x += 10
        self.draw()

    def move_up(self):
        self.y -= 10
        self.draw()

    def move_down(self):
        self.y += 10
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


if __name__ == '__main__':
    game = Game()
    game.run()
