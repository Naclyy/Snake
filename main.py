import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (153, 255, 255)

SCREEN_WIDTH = SIZE * 25
SCREEN_HEIGHT = SIZE * 20


class Apple:
    def __init__(self, surface):
        self.image = pygame.image.load("resource/apple.png")
        self.parent_screen = surface

        self.x = random.randint(1, int((SCREEN_WIDTH - SIZE) / SIZE)) * SIZE
        self.y = random.randint(1, int((SCREEN_HEIGHT - SIZE) / SIZE)) * SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, int((SCREEN_WIDTH - SIZE) / SIZE)) * SIZE
        self.y = random.randint(1, int((SCREEN_HEIGHT - SIZE) / SIZE)) * SIZE


class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        self.block = pygame.image.load("resource/snake_body.png")
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

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

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        self.draw()


def is_collision(x1, y1, x2, y2):
    if x2 <= x1 < x2 + SIZE:
        if y2 <= y1 < y2 + SIZE:
            return True
    return False


class Game:
    def __init__(self):
        pygame.init()

        # this is the game window
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # change the screen color
        self.surface.fill(BACKGROUND_COLOR)

        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        loop = True
        pause = False
        while loop:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        loop = False
                    if event.key == K_RETURN:
                        pause = False
                    if not pause:
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
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial', 30)
        game_over = font.render(f"Game is over! Your score is: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(game_over, (120, 320))
        play_again = font.render(f"To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(play_again, (240, 350))
        pygame.display.flip()

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (SCREEN_WIDTH - SIZE * 5, SIZE))

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with apple
        if is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game Over"

        # snake colliding with screen border
        if self.snake.x[0] < 0 and self.snake.direction == 'left' \
                or self.snake.x[0] > SCREEN_WIDTH - SIZE and self.snake.direction == 'right' \
                or self.snake.y[0] < 0 and self.snake.direction == 'up' \
                or self.snake.y[0] > SCREEN_HEIGHT - SIZE and self.snake.direction == 'down':
            raise "Game Over"


if __name__ == '__main__':
    game = Game()
    game.run()
