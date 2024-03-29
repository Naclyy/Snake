import json
import sys

import pygame
from pygame.locals import *
import time
import random
import numpy

# variable used to test if the program got any argument
DEFAULT = 1
if len(sys.argv) == 2:
    DEFAULT = 0
    f = open(sys.argv[1], "r")
    data = json.loads(f.read())
    X = data["x"]
    Y = data["y"]
else:
    X = 20
    Y = 20
SIZE = 40
BACKGROUND_COLOR = (0, 230, 0)
GRASS_COLOR = (0, 179, 0)
SCREEN_WIDTH = SIZE * X
SCREEN_HEIGHT = SIZE * Y
CURRENT_HIGH_SCORE = 0
LETTER_COLOUR = (204, 0, 0)
FONT_SIZE = X + Y
NIGHT_MODE = False
NIGHT_MODE_BACKGROUND_COLOR = (111, 104, 104)
NIGHT_MODE_GRASS_COLOR = (30, 29, 29)
MUTED = False

# sets the default difficulty
DIFFICULTY = 'MEDIUM'


def play_sound(type_of_sound):
    """
    Callable used to play sound for eating apple or crashing the snake.
    """
    sound = ""
    if type_of_sound == 'eat_apple':
        sound = pygame.mixer.Sound("resource/Minecraft Eating - Sound Effect (HD).mp3")
    if type_of_sound == 'crash':
        sound = pygame.mixer.Sound("resource/video game over sound effect.mp3")
    pygame.mixer.Sound.play(sound)


def play_background():
    """
    Callable used to play the background music.
    """
    pygame.mixer.music.load("resource/Theme (30 minutes).mp3")
    pygame.mixer.music.play()


def draw_text(text, size, x_position, y_position, surface):
    """
    Callable used to draw text on given position on the screen.
    :return: Rect that has the text
    :rtype: Rect
    """
    font_name = pygame.font.get_default_font()
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, LETTER_COLOUR)
    text_rect = text_surface.get_rect()
    text_rect.center = (x_position, y_position)
    surface.blit(text_surface, text_rect)
    return text_rect


def is_collision(x1, y1, x2, y2):
    """
    Callable used to test if two points collide.
    :return: True or False if they collide or not
    :rtype: Boolean
    """
    if x2 <= x1 < x2 + SIZE:
        if y2 <= y1 < y2 + SIZE:
            return True
    return False


class Rock:
    """
    Class used to create the obstacle logic.
    """

    def __init__(self, surface):
        self.image = pygame.image.load("resource/rock.png")
        self.parent_screen = surface
        self.x = []
        self.y = []
        self.number_of_rocks = 0

    def add_rock(self, x, y):
        """
        Callable used to add obstacle to the vector.
        """
        self.x.append(x)
        self.y.append(y)
        self.number_of_rocks += 1

    def draw(self):
        """
        Callable used to print the obstacles on the screen
        """
        for i in range(self.number_of_rocks):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()


class Apple:
    """
    Class used to create the apple logic.
    """

    def __init__(self, surface, snake, rock):
        self.image = pygame.image.load("resource/apple.png")
        self.parent_screen = surface
        self.snake = snake
        self.rock = rock
        self.obstacle_matrix = numpy.zeros((X, Y))
        self.add_rocks_to_matrix()
        self.x, self.y = self.generate_apple()

    def generate_apple(self):
        """
        Callable used to generate the apple x and y depending on the obstacle matrix.
        """
        free_space = []
        for i in range(X):
            for j in range(Y):
                if self.obstacle_matrix[i][j] == 0:
                    free_space.append([i, j])
        random_apple_spot = random.randint(1, len(free_space) - 1)
        return free_space[random_apple_spot][0] * SIZE, free_space[random_apple_spot][1] * SIZE

    def add_rocks_to_matrix(self):
        """
        Callable used to add the obstacle positions to the obstacle matrix.
        """
        for i in range(self.rock.number_of_rocks):
            if self.rock.x[i] / SIZE < X and self.rock.y[i] / SIZE < Y:
                self.obstacle_matrix[int(self.rock.x[i] / SIZE)][int(self.rock.y[i] / SIZE)] = 1

    def draw(self):
        """
        Callable used to draw the apple.
        """
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        """
        Callable used to generate a new position for the apple without it being on top of the snake or obstacle.
        """
        self.obstacle_matrix = numpy.zeros((X, Y))
        self.add_rocks_to_matrix()
        for i in range(self.snake.length):
            self.obstacle_matrix[int(self.snake.x[i] / SIZE)][int(self.snake.y[i] / SIZE)] = 1
        self.x, self.y = self.generate_apple()


class Snake:
    """
    Class used to create the Snake logic.
    """

    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'
        if not NIGHT_MODE:
            self.night_mode = False
        else:
            self.night_mode = True

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

    def draw_grass(self):
        """
        Callable used to draw the grass to the table.
        """
        for row in range(SCREEN_WIDTH):
            if row % 2 == 0:
                for col in range(SCREEN_HEIGHT):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * SIZE, row * SIZE, SIZE, SIZE)
                        if not self.night_mode:
                            pygame.draw.rect(self.parent_screen, GRASS_COLOR, grass_rect)
                        else:
                            pygame.draw.rect(self.parent_screen, NIGHT_MODE_GRASS_COLOR, grass_rect)
            else:
                for col in range(SCREEN_HEIGHT):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * SIZE, row * SIZE, SIZE, SIZE)
                        if not self.night_mode:
                            pygame.draw.rect(self.parent_screen, GRASS_COLOR, grass_rect)
                        else:
                            pygame.draw.rect(self.parent_screen, NIGHT_MODE_GRASS_COLOR, grass_rect)

    def draw(self):
        """
        Callable used to draw the snake and table.
        """
        if not self.night_mode:
            self.parent_screen.fill(BACKGROUND_COLOR)
        else:
            self.parent_screen.fill(NIGHT_MODE_BACKGROUND_COLOR)
        self.draw_grass()
        for i in range(self.length):
            if i == 0:
                if self.direction == 'right':
                    self.parent_screen.blit(self.head_right, (self.x[i], self.y[i]))
                elif self.direction == 'left':
                    self.parent_screen.blit(self.head_left, (self.x[i], self.y[i]))
                elif self.direction == 'up':
                    self.parent_screen.blit(self.head_up, (self.x[i], self.y[i]))
                elif self.direction == 'down':
                    self.parent_screen.blit(self.head_down, (self.x[i], self.y[i]))
            elif i == self.length - 1:
                if self.x[i] < self.x[i - 1]:
                    self.parent_screen.blit(self.tail_left, (self.x[i], self.y[i]))
                elif self.x[i] > self.x[i - 1]:
                    self.parent_screen.blit(self.tail_right, (self.x[i], self.y[i]))
                elif self.y[i] < self.y[i - 1]:
                    self.parent_screen.blit(self.tail_up, (self.x[i], self.y[i]))
                elif self.y[i] > self.y[i - 1]:
                    self.parent_screen.blit(self.tail_down, (self.x[i], self.y[i]))
            else:
                if (self.x[i + 1] > self.x[i] > self.x[i - 1] or self.x[i + 1] < self.x[i] < self.x[i - 1]) and \
                        self.y[i] == self.y[i + 1] == self.y[i - 1]:
                    self.parent_screen.blit(self.body_horizontal, (self.x[i], self.y[i]))
                elif (self.y[i + 1] > self.y[i] > self.y[i - 1] or self.y[i + 1] < self.y[i] < self.y[i - 1]) and \
                        self.x[i] == self.x[i + 1] == self.x[i - 1]:
                    self.parent_screen.blit(self.body_vertical, (self.x[i], self.y[i]))
                elif (self.x[i] < self.x[i + 1] and self.x[i] == self.x[i - 1]
                      and self.y[i] == self.y[i + 1] and self.y[i] < self.y[i - 1]) \
                        or (self.x[i] < self.x[i - 1] and self.x[i] == self.x[i + 1]
                            and self.y[i] == self.y[i - 1] and self.y[i] < self.y[i + 1]):
                    self.parent_screen.blit(self.body_br, (self.x[i], self.y[i]))
                elif (self.x[i] > self.x[i + 1] and self.x[i] == self.x[i - 1]
                      and self.y[i] == self.y[i + 1] and self.y[i] > self.y[i - 1]) \
                        or (self.x[i] > self.x[i - 1] and self.x[i] == self.x[i + 1]
                            and self.y[i] == self.y[i - 1] and self.y[i] > self.y[i + 1]):
                    self.parent_screen.blit(self.body_tl, (self.x[i], self.y[i]))
                elif (self.x[i] < self.x[i + 1] and self.x[i] == self.x[i - 1]
                      and self.y[i] == self.y[i + 1] and self.y[i] > self.y[i - 1]) \
                        or (self.x[i] < self.x[i - 1] and self.x[i] == self.x[i + 1]
                            and self.y[i] == self.y[i - 1] and self.y[i] > self.y[i + 1]):
                    self.parent_screen.blit(self.body_tr, (self.x[i], self.y[i]))
                elif (self.x[i] > self.x[i + 1] and self.x[i] == self.x[i - 1]
                      and self.y[i] == self.y[i + 1] and self.y[i] < self.y[i - 1]) \
                        or (self.x[i] > self.x[i - 1] and self.x[i] == self.x[i + 1]
                            and self.y[i] == self.y[i - 1] and self.y[i] < self.y[i + 1]):
                    self.parent_screen.blit(self.body_bl, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        """
        Callable used to increase the length of the snake.
        """
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        """
        Callable used to change the direction of the snake to left.
        """
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        """
        Callable used to change the direction of the snake to right.
        """
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        """
        Callable used to change the direction of the snake to up.
        """
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        """
        Callable used to change the direction of the snake to down.
        """
        if self.direction != 'up':
            self.direction = 'down'

    def walk(self):
        """
        Callable used to make the appearance of snake walking.
        """
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


class Play:
    """
    Class used to create the snake game logic.
    """

    def __init__(self, surface):
        self.surface = surface
        self.click = False
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.rock = Rock(self.surface)
        self.read_rocks_from_file()
        self.apple = Apple(self.surface, self.snake, self.rock)
        self.apple.draw()

    def reset(self):
        """
        Callable used to reset the game.
        """
        self.snake = Snake(self.surface, 2)
        self.apple = Apple(self.surface, self.snake, self.rock)

    def run(self):
        """
        Callable used to start the game.
        """
        global MUTED, NIGHT_MODE
        loop = True
        pause = False
        while loop:
            self.click = False
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
                if event.type == KEYDOWN:
                    if event.key == K_m:
                        if not pause:
                            if not MUTED:
                                MUTED = True
                                pygame.mixer.music.stop()
                            else:
                                MUTED = False
                                pygame.mixer.music.play()
                    if event.key == K_n:
                        if not NIGHT_MODE:
                            NIGHT_MODE = True
                            self.snake.night_mode = True
                        else:
                            NIGHT_MODE = False
                            self.snake.night_mode = False
                    if event.key == K_ESCAPE:
                        self.reset()
                        pygame.mixer.music.stop()
                        return
                    if event.key == K_RETURN:
                        if pause:
                            if not MUTED:
                                pygame.mixer.music.play()
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
                    exit()
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            if DIFFICULTY == 'MEDIUM':
                time.sleep(0.6)
            elif DIFFICULTY == 'HARD':
                time.sleep(0.3)
            elif DIFFICULTY == 'EXTREME':
                time.sleep(0.1)
            else:
                time.sleep(0.9)

    def read_rocks_from_file(self):
        """
        Callable used to read the obstacles from json.
        """
        if DEFAULT == 0:
            for i in range(len(data["obstacle_list"])):
                self.rock.add_rock(data["obstacle_list"][i][0] * SIZE, data["obstacle_list"][i][1] * SIZE)
            self.rock.draw()

    def show_game_over(self):
        """
        Callable used to create the game over screen.
        """
        global CURRENT_HIGH_SCORE
        # create background
        self.surface.fill("white")
        background_picture = pygame.image.load("resource/snake_background.png")
        background_picture = pygame.transform.scale(background_picture, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface.blit(background_picture, (0, 0))

        draw_text(f"Play is over! Your score is: {self.snake.length}", FONT_SIZE, SCREEN_WIDTH / 2, FONT_SIZE * 4,
                  self.surface)

        if CURRENT_HIGH_SCORE < self.snake.length:
            CURRENT_HIGH_SCORE = self.snake.length
            draw_text(f"You've beaten your HighScore!!!", FONT_SIZE, SCREEN_WIDTH / 2,
                      SCREEN_HEIGHT / 2 - FONT_SIZE * 2, self.surface)
        else:
            draw_text(f"Your current HighScore is {CURRENT_HIGH_SCORE}", FONT_SIZE, SCREEN_WIDTH / 2,
                      SCREEN_HEIGHT / 2 - FONT_SIZE * 2, self.surface)

        draw_text(f"To play again press Enter.", FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, self.surface)
        draw_text(f"To exit press Escape.", FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 2,
                  self.surface)

        pygame.display.flip()

        pygame.mixer.music.stop()

    def display_score(self):
        """
        Callable used to display the score on the bottom right of the screen.
        """
        # set the font
        font = pygame.font.SysFont('roboto', FONT_SIZE)
        score = font.render(f"1", True, "red")
        if self.snake.length > 2:
            if DIFFICULTY == 'EASY':
                score = font.render(f"{self.snake.length - 1}", True, "red")
            elif DIFFICULTY == 'MEDIUM':
                score = font.render(f"{(self.snake.length - 1) * 2}", True, "red")
            elif DIFFICULTY == 'HARD':
                score = font.render(f"{(self.snake.length - 1) * 3}", True, "red")
            elif DIFFICULTY == 'EXTREME':
                score = font.render(f"{(self.snake.length - 1) * 5}", True, "red")
        score_x = int(SCREEN_WIDTH - SIZE + 5)
        score_y = int(SCREEN_HEIGHT - SIZE)
        score_rect = score.get_rect(center=(score_x, score_y))

        apple_image = pygame.image.load("resource/apple.png")
        apple_rect = apple_image.get_rect(midright=(score_rect.left, score_rect.centery))

        # Create the border
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 10,
                              apple_rect.height)
        pygame.draw.rect(self.surface, "black", bg_rect, 3)

        self.surface.blit(apple_image, apple_rect)
        self.surface.blit(score, score_rect)

    def play(self):
        """
        Callable used to play the game logic.
        """
        self.snake.walk()
        self.apple.draw()
        self.rock.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with apple
        if is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            play_sound("eat_apple")
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                play_sound("crash")
                raise "Play Over"

        # snake colliding with screen border
        if self.snake.x[0] < 0 and self.snake.direction == 'left' \
                or self.snake.x[0] > SCREEN_WIDTH - SIZE and self.snake.direction == 'right' \
                or self.snake.y[0] < 0 and self.snake.direction == 'up' \
                or self.snake.y[0] > SCREEN_HEIGHT - SIZE and self.snake.direction == 'down':
            play_sound("crash")
            raise "Play Over"

        # snake colliding with rock
        for i in range(self.rock.number_of_rocks):
            if is_collision(self.snake.x[0], self.snake.y[0], self.rock.x[i], self.rock.y[i]):
                play_sound("crash")
                raise "Play Over"


class Help:
    """
    Class used to create the help screen.
    """

    def __init__(self, surface):
        self.click = False
        self.surface = surface

    def help_screen(self):
        """
        Callable used to display information on the help screen.
        """
        loop = True
        while loop:

            self.surface.fill(GRASS_COLOR)
            draw_text('How to play the game:', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - FONT_SIZE * 6,
                      self.surface)
            draw_text('W, A, S, D - to move the snake', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - FONT_SIZE * 2,
                      self.surface)
            draw_text('N - to activate night mode', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, self.surface)
            draw_text('M - to mute the music', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 2,
                      self.surface)
            draw_text('ESC - to go back', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 4, self.surface)
            back_button = draw_text('Go back', int(FONT_SIZE / 2), SCREEN_WIDTH / 2 - FONT_SIZE * 8,
                                    SCREEN_HEIGHT - FONT_SIZE, self.surface)
            pygame.display.flip()

            mx, my = pygame.mouse.get_pos()

            if back_button.collidepoint((mx, my)):
                if self.click is True:
                    loop = False
            self.click = False
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        loop = False
                if event.type == QUIT:
                    exit()


class Option:
    """
    Class used to create the option screen.
    """

    def __init__(self, surface):
        self.click = False
        self.surface = surface
        self.cursor_rect_options = pygame.Rect(0, 0, 0, 0)
        self.cursor_rect_selected = pygame.Rect(0, 0, 0, 0)

    def move_cursor_for_options(self, state, key):
        """
        Callable used to move the pointing cursor.
        """
        if key == 'Down':
            if state == 'EASY':
                self.cursor_rect_options.center = (SCREEN_WIDTH / 2 - FONT_SIZE * 3, SCREEN_HEIGHT / 2 - FONT_SIZE / 8)
                return 'MEDIUM'
            elif state == 'MEDIUM':
                self.cursor_rect_options.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 2 - FONT_SIZE / 4, SCREEN_HEIGHT / 2 + FONT_SIZE * 2 - FONT_SIZE / 8)
                return 'HARD'
            elif state == 'HARD':
                self.cursor_rect_options.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 3 - FONT_SIZE / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 4 - FONT_SIZE / 8)
                return 'EXTREME'
            elif state == 'EXTREME':
                self.cursor_rect_options.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 2 - FONT_SIZE / 4, SCREEN_HEIGHT / 2 - FONT_SIZE * 2 - FONT_SIZE / 8)
                return 'EASY'
        elif key == 'Up':
            if state == 'EASY':
                self.cursor_rect_options.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 3 - FONT_SIZE / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 4 - FONT_SIZE / 8)
                return 'EXTREME'
            elif state == 'MEDIUM':
                self.cursor_rect_options.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 2 - FONT_SIZE / 4, SCREEN_HEIGHT / 2 - FONT_SIZE * 2 - FONT_SIZE / 8)
                return 'EASY'
            elif state == 'HARD':
                self.cursor_rect_options.center = (SCREEN_WIDTH / 2 - FONT_SIZE * 3, SCREEN_HEIGHT / 2 - FONT_SIZE / 8)
                return 'MEDIUM'
            elif state == 'EXTREME':
                self.cursor_rect_options.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 2 - FONT_SIZE / 4, SCREEN_HEIGHT / 2 + FONT_SIZE * 2 - FONT_SIZE / 8)
                return 'HARD'
        elif key == 'Mouse':
            if state == 'EASY':
                self.cursor_rect_options.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 2 - FONT_SIZE / 4, SCREEN_HEIGHT / 2 - FONT_SIZE * 2 + FONT_SIZE / 8)
                return 'EASY'
            elif state == 'MEDIUM':
                self.cursor_rect_options.center = (SCREEN_WIDTH / 2 - FONT_SIZE * 3, SCREEN_HEIGHT / 2 + FONT_SIZE / 8)
                return 'MEDIUM'
            elif state == 'HARD':
                self.cursor_rect_options.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 2 - FONT_SIZE / 4, SCREEN_HEIGHT / 2 + FONT_SIZE * 2 + FONT_SIZE / 8)
                return 'HARD'
            elif state == 'EXTREME':
                self.cursor_rect_options.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 3 - FONT_SIZE / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 4 + FONT_SIZE / 8)
                return 'EXTREME'

    def option_screen(self):
        """
        Callable used to display information on the option screen.
        """
        global DIFFICULTY
        state = 'EASY'
        loop = True
        self.cursor_rect_options.center = (
            SCREEN_WIDTH / 2 - FONT_SIZE * 2 - FONT_SIZE / 4, SCREEN_HEIGHT / 2 - FONT_SIZE * 2 - FONT_SIZE / 8)
        while loop:
            self.surface.fill(GRASS_COLOR)
            self.selected_option(DIFFICULTY)
            self.draw_selected_cursor()
            self.draw_option_cursor()
            draw_text('Select Difficulty:', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - FONT_SIZE * 6,
                      self.surface)
            easy = draw_text('EASY', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - FONT_SIZE * 2, self.surface)
            medium = draw_text('MEDIUM', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, self.surface)
            hard = draw_text('HARD', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 2, self.surface)
            extreme = draw_text('EXTREME', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 4, self.surface)
            back_button = draw_text('Go back', int(FONT_SIZE / 2), SCREEN_WIDTH / 2 - FONT_SIZE * 8,
                                    SCREEN_HEIGHT - FONT_SIZE, self.surface)
            pygame.display.flip()

            mx, my = pygame.mouse.get_pos()

            if back_button.collidepoint((mx, my)):
                if self.click is True:
                    self.click = False
                    loop = False
            if easy.collidepoint((mx, my)):
                state = self.move_cursor_for_options('EASY', 'Mouse')
                if self.click is True:
                    self.click = False
                    DIFFICULTY = 'EASY'
            if medium.collidepoint((mx, my)):
                state = self.move_cursor_for_options('MEDIUM', 'Mouse')
                if self.click is True:
                    self.click = False
                    DIFFICULTY = 'MEDIUM'
            if hard.collidepoint((mx, my)):
                state = self.move_cursor_for_options('HARD', 'Mouse')
                if self.click is True:
                    self.click = False
                    DIFFICULTY = 'HARD'
            if extreme.collidepoint((mx, my)):
                state = self.move_cursor_for_options('EXTREME', 'Mouse')
                if self.click is True:
                    self.click = False
                    DIFFICULTY = 'EXTREME'
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        state = self.move_cursor_for_options(state, 'Up')
                    if event.key == K_DOWN:
                        state = self.move_cursor_for_options(state, 'Down')
                    if event.key == K_RETURN:
                        DIFFICULTY = state
                    if event.key == K_ESCAPE:
                        loop = False
                if event.type == QUIT:
                    exit()

    def draw_option_cursor(self):
        draw_text('*', FONT_SIZE, self.cursor_rect_options.x, self.cursor_rect_options.y, self.surface)

    def draw_selected_cursor(self):
        draw_text('<-', FONT_SIZE, self.cursor_rect_selected.x, self.cursor_rect_selected.y, self.surface)

    def selected_option(self, difficulty):
        """
        Callable used to move the selected cursor.
        """
        if difficulty == 'EASY':
            self.cursor_rect_selected.center = (
                SCREEN_WIDTH / 2 + FONT_SIZE * 2 + FONT_SIZE / 4, SCREEN_HEIGHT / 2 - FONT_SIZE * 2 - FONT_SIZE / 8)
        elif difficulty == 'MEDIUM':
            self.cursor_rect_selected.center = (SCREEN_WIDTH / 2 + FONT_SIZE * 3, SCREEN_HEIGHT / 2 - FONT_SIZE / 8)
        elif difficulty == 'HARD':
            self.cursor_rect_selected.center = (
                SCREEN_WIDTH / 2 + FONT_SIZE * 2 + FONT_SIZE / 4, SCREEN_HEIGHT / 2 + FONT_SIZE * 2 - FONT_SIZE / 8)
        elif difficulty == 'EXTREME':
            self.cursor_rect_selected.center = (
                SCREEN_WIDTH / 2 + FONT_SIZE * 3 + FONT_SIZE / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 4 - FONT_SIZE / 8)


class Menu:
    """
    Class used to create the menu screen.
    """

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # this is the game window
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.cursor_rect_menu = pygame.Rect(0, 0, 0, 0)
        self.click = False

    def draw_menu_cursor(self):
        draw_text('*', FONT_SIZE, self.cursor_rect_menu.x, self.cursor_rect_menu.y, self.surface)

    def move_cursor_for_menu(self, state, key):
        """
        Callable used to move the pointing cursor.
        """
        if key == 'Down':
            if state == 'Start':
                self.cursor_rect_menu.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 3, SCREEN_HEIGHT / 2 - FONT_SIZE * 2 + FONT_SIZE / 4)
                return 'Options'
            elif state == 'Options':
                self.cursor_rect_menu.center = (SCREEN_WIDTH / 2 - FONT_SIZE * 2, SCREEN_HEIGHT / 2 + FONT_SIZE / 4)
                return 'Help'
            elif state == 'Help':
                self.cursor_rect_menu.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 2 + FONT_SIZE / 4, SCREEN_HEIGHT / 2 + FONT_SIZE * 2 + FONT_SIZE / 4)
                return 'Exit'
            elif state == 'Exit':
                self.cursor_rect_menu.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 4, SCREEN_HEIGHT / 2 - FONT_SIZE * 4 + FONT_SIZE / 4)
                return 'Start'
        elif key == 'Up':
            if state == 'Start':
                self.cursor_rect_menu.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 2 + 10, SCREEN_HEIGHT / 2 + FONT_SIZE * 2 + FONT_SIZE / 4)
                return 'Exit'
            elif state == 'Options':
                self.cursor_rect_menu.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 4, SCREEN_HEIGHT / 2 - FONT_SIZE * 4 + FONT_SIZE / 4)
                return 'Start'
            elif state == 'Help':
                self.cursor_rect_menu.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 3, SCREEN_HEIGHT / 2 - FONT_SIZE * 2 + FONT_SIZE / 4)
                return 'Options'
            elif state == 'Exit':
                self.cursor_rect_menu.center = (SCREEN_WIDTH / 2 - FONT_SIZE * 2, SCREEN_HEIGHT / 2 + FONT_SIZE / 4)
                return 'Help'
        elif key == 'Mouse':
            if state == 'Start':
                self.cursor_rect_menu.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 4, SCREEN_HEIGHT / 2 - FONT_SIZE * 4 + FONT_SIZE / 4)
                return 'Start'
            elif state == 'Options':
                self.cursor_rect_menu.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 3, SCREEN_HEIGHT / 2 - FONT_SIZE * 2 + FONT_SIZE / 4)
                return 'Options'
            elif state == 'Help':
                self.cursor_rect_menu.center = (SCREEN_WIDTH / 2 - FONT_SIZE * 2, SCREEN_HEIGHT / 2 + FONT_SIZE / 4)
                return 'Help'
            elif state == 'Exit':
                self.cursor_rect_menu.center = (
                    SCREEN_WIDTH / 2 - FONT_SIZE * 2 + 10, SCREEN_HEIGHT / 2 + FONT_SIZE * 2 + FONT_SIZE / 4)
                return 'Exit'

    def menu(self):
        """
        Callable used to display the menu screen.
        """
        state = 'Start'
        self.cursor_rect_menu.center = (
            SCREEN_WIDTH / 2 - FONT_SIZE * 4, SCREEN_HEIGHT / 2 - FONT_SIZE * 4 + FONT_SIZE / 4)

        loop = True
        while loop:
            # set the menu background
            self.surface.fill("white")
            background_picture = pygame.image.load("resource/snake_background.png")
            background_picture = pygame.transform.scale(background_picture, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.surface.blit(background_picture, (0, 0))
            self.draw_menu_cursor()

            # get mouse coordinates
            mx, my = pygame.mouse.get_pos()

            play_button = draw_text('Start Play', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - FONT_SIZE * 4,
                                    self.surface)
            options_button = draw_text('Options', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - FONT_SIZE * 2,
                                       self.surface)
            help_button = draw_text('Help', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 0, self.surface)
            exit_button = draw_text('Exit', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 2,
                                    self.surface)
            if play_button.collidepoint((mx, my)):
                state = self.move_cursor_for_menu('Start', 'Mouse')
                if self.click is True:
                    play_background()
                    Play(self.surface).run()
            if options_button.collidepoint((mx, my)):
                state = self.move_cursor_for_menu('Options', 'Mouse')
                if self.click is True:
                    self.click = False
                    Option(self.surface).option_screen()
            if help_button.collidepoint((mx, my)):
                state = self.move_cursor_for_menu('Help', 'Mouse')
                if self.click is True:
                    self.click = False
                    Help(self.surface).help_screen()
            if exit_button.collidepoint((mx, my)):
                state = self.move_cursor_for_menu('Exit', 'Mouse')
                if self.click is True:
                    exit()

            pygame.display.flip()
            self.click = False
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pass
                    if event.key == K_UP:
                        state = self.move_cursor_for_menu(state, 'Up')
                    if event.key == K_DOWN:
                        state = self.move_cursor_for_menu(state, 'Down')
                    if event.key == K_RETURN:
                        if state == 'Start':
                            play_background()
                            Play(self.surface).run()
                        elif state == 'Options':
                            Option(self.surface).option_screen()
                        elif state == 'Help':
                            Help(self.surface).help_screen()
                        elif state == 'Exit':
                            exit()
                elif event.type == QUIT:
                    exit()


if __name__ == '__main__':
    game = Menu()
    game.menu()
