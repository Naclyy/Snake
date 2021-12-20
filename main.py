import pygame
from pygame.locals import *
import time
import random

SIZE = 40
X = 20
Y = 20
BACKGROUND_COLOR = (0, 230, 0)
GRASS_COLOR = (0, 179, 0)
SCREEN_WIDTH = SIZE * X
SCREEN_HEIGHT = SIZE * Y
CURRENT_HIGH_SCORE = 0
LETTER_COLOUR = (204, 0, 0)
FONT_SIZE = X + Y
NIGHT_MODE = False
NIGHT_MODE_BACKGROUND_COLOR = (76, 31, 255)
NIGHT_MODE_GRASS_COLOR = (29, 0, 145)
MUTED = False
DIFFICULTY = 'EASY'


class Tree:
    def __init__(self, surface):
        self.image = pygame.image.load("resource/tree.png")
        self.parent_screen = surface
        self.x = []
        self.y = []
        self.number_of_trees = 0

    def add_tree(self, x, y):
        self.x.append(x)
        self.y.append(y)
        self.number_of_trees += 1

    def draw(self):
        for i in range(self.number_of_trees):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()


class Apple:
    def __init__(self, surface, snake, tree):
        self.image = pygame.image.load("resource/apple.png")
        self.parent_screen = surface
        self.snake = snake
        self.tree = tree
        self.x = random.randint(1, int((SCREEN_WIDTH - SIZE) / SIZE)) * SIZE
        self.y = random.randint(1, int((SCREEN_HEIGHT - SIZE) / SIZE)) * SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        # needs improvement for the randomness
        # logic so it wont appear on top of the snake (i)
        # logic so it wont appear on top of the tree (j)
        i = 0
        j = 0
        while i < self.snake.length and j < self.tree.number_of_trees:
            if is_collision(self.snake.x[i], self.snake.y[i], self.x, self.y) or is_collision(self.tree.x[j],
                                                                                              self.tree.y[j], self.x,
                                                                                              self.y):
                self.x = random.randint(1, int((SCREEN_WIDTH - SIZE) / SIZE)) * SIZE
                self.y = random.randint(1, int((SCREEN_HEIGHT - SIZE) / SIZE)) * SIZE
                i = 0
                j = 0
            else:
                if i < self.snake.length:
                    i += 1
                if j < self.tree.number_of_trees:
                    j += 1


class Snake:
    def __init__(self, surface, length):
        self.length = length
        self.parent_screen = surface
        self.block = pygame.image.load("resource/snake_body.png")
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'
        if not NIGHT_MODE:
            self.night_mode = False
        else:
            self.night_mode = True

    def draw_grass(self):
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
        if not self.night_mode:
            self.parent_screen.fill(BACKGROUND_COLOR)
        else:
            self.parent_screen.fill(NIGHT_MODE_BACKGROUND_COLOR)
        self.draw_grass()
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

    def draw_menu_cursor(self):
        self.draw_text('*', FONT_SIZE, self.cursor_rect_menu.x, self.cursor_rect_menu.y)

    def move_cursor_for_menu(self, state, key):
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

    def __init__(self):
        self.cursor_rect_menu = pygame.Rect(0, 0, 0, 0)
        self.cursor_rect_options = pygame.Rect(0, 0, 0, 0)
        self.cursor_rect_selected = pygame.Rect(0, 0, 0, 0)
        pygame.init()
        pygame.mixer.init()
        # this is the game window
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.click = False
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.tree = Tree(self.surface)
        self.read_trees_from_file()
        self.apple = Apple(self.surface, self.snake, self.tree)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface, self.snake, self.tree)

    def run(self):
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
                time.sleep(0.3)
            elif DIFFICULTY == 'HARD':
                time.sleep(0.2)
            elif DIFFICULTY == 'EXTREME':
                time.sleep(0.1)
            else:
                time.sleep(0.5)

    def menu(self):
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

            play_button = self.draw_text('Start Game', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - FONT_SIZE * 4)
            options_button = self.draw_text('Options', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - FONT_SIZE * 2)
            help_button = self.draw_text('Help', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 0)
            exit_button = self.draw_text('Exit', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 2)
            if play_button.collidepoint((mx, my)):
                state = self.move_cursor_for_menu('Start', 'Mouse')
                if self.click is True:
                    play_background()
                    self.run()
            if options_button.collidepoint((mx, my)):
                state = self.move_cursor_for_menu('Options', 'Mouse')
                if self.click is True:
                    self.click = False
                    self.option_screen()
            if help_button.collidepoint((mx, my)):
                state = self.move_cursor_for_menu('Help', 'Mouse')
                if self.click is True:
                    self.click = False
                    self.help_screen()
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
                            self.run()
                        elif state == 'Options':
                            self.option_screen()
                        elif state == 'Help':
                            self.help_screen()
                        elif state == 'Exit':
                            exit()
                elif event.type == QUIT:
                    exit()

    def draw_text(self, text, size, x, y):
        font_name = pygame.font.get_default_font()
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, LETTER_COLOUR)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.surface.blit(text_surface, text_rect)
        return text_rect

    def help_screen(self):
        loop = True
        while loop:

            self.surface.fill(GRASS_COLOR)
            self.draw_text('How to play the game:', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - FONT_SIZE * 6)
            self.draw_text('W, A, S, D - to move the snake', FONT_SIZE, SCREEN_WIDTH / 2,
                           SCREEN_HEIGHT / 2 - FONT_SIZE * 2)
            self.draw_text('N - to activate night mode', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            self.draw_text('M - to mute the music', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 2)
            self.draw_text('ESC - to go back', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 4)
            back_button = self.draw_text('Go back', int(FONT_SIZE / 2), SCREEN_WIDTH / 2 - FONT_SIZE * 8,
                                         SCREEN_HEIGHT - FONT_SIZE)
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

    def move_cursor_for_options(self, state, key):
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
        global DIFFICULTY
        state = 'EASY'
        loop = True
        while loop:
            self.surface.fill(GRASS_COLOR)
            self.selected_option(DIFFICULTY)
            self.draw_selected_cursor()
            self.draw_option_cursor()
            self.draw_text('Select Difficulty:', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - FONT_SIZE * 6)
            easy = self.draw_text('EASY', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - FONT_SIZE * 2)
            medium = self.draw_text('MEDIUM', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            hard = self.draw_text('HARD', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 2)
            extreme = self.draw_text('EXTREME', FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 4)
            back_button = self.draw_text('Go back', int(FONT_SIZE / 2), SCREEN_WIDTH / 2 - FONT_SIZE * 8,
                                         SCREEN_HEIGHT - FONT_SIZE)
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
        self.draw_text('*', FONT_SIZE, self.cursor_rect_options.x, self.cursor_rect_options.y)

    def draw_selected_cursor(self):
        self.draw_text('<-', FONT_SIZE, self.cursor_rect_selected.x, self.cursor_rect_selected.y)

    def selected_option(self, difficulty):
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

    def read_trees_from_file(self):
        file = open("trees_position.txt", "r")
        for tree_coordinate in file:
            self.tree.add_tree(int(tree_coordinate[0]) * SIZE, int(tree_coordinate[2]) * SIZE)
        self.tree.draw()

    def show_game_over(self):
        global CURRENT_HIGH_SCORE
        # create background
        self.surface.fill("white")
        background_picture = pygame.image.load("resource/snake_background.png")
        background_picture = pygame.transform.scale(background_picture, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface.blit(background_picture, (0, 0))

        self.draw_text(f"Game is over! Your score is: {self.snake.length}", FONT_SIZE, SCREEN_WIDTH / 2, FONT_SIZE * 4)

        if CURRENT_HIGH_SCORE < self.snake.length:
            CURRENT_HIGH_SCORE = self.snake.length
            self.draw_text(f"You've beaten your HighScore!!!", FONT_SIZE, SCREEN_WIDTH / 2,
                           SCREEN_HEIGHT / 2 - FONT_SIZE * 2)
        else:
            self.draw_text(f"Your current HighScore is {CURRENT_HIGH_SCORE}", FONT_SIZE, SCREEN_WIDTH / 2,
                           SCREEN_HEIGHT / 2 - FONT_SIZE * 2)

        self.draw_text(f"To play again press Enter.", FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.draw_text(f"To exit press Escape.", FONT_SIZE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 2)

        pygame.display.flip()

        pygame.mixer.music.stop()

    def display_score(self):
        # set the font
        font = pygame.font.SysFont('roboto', FONT_SIZE)

        score = font.render(f"{self.snake.length}", True, "red")
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
        self.snake.walk()
        self.apple.draw()
        self.tree.draw()
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
                raise "Game Over"

        # snake colliding with screen border
        if self.snake.x[0] < 0 and self.snake.direction == 'left' \
                or self.snake.x[0] > SCREEN_WIDTH - SIZE and self.snake.direction == 'right' \
                or self.snake.y[0] < 0 and self.snake.direction == 'up' \
                or self.snake.y[0] > SCREEN_HEIGHT - SIZE and self.snake.direction == 'down':
            play_sound("crash")
            raise "Game Over"

        # snake colliding with tree
        for i in range(self.tree.number_of_trees):
            if is_collision(self.snake.x[0], self.snake.y[0], self.tree.x[i], self.tree.y[i]):
                play_sound("crash")
                raise "Game Over"


def play_sound(type_of_sound):
    sound = ""
    if type_of_sound == 'eat_apple':
        sound = pygame.mixer.Sound("resource/Minecraft Eating - Sound Effect (HD).mp3")
    if type_of_sound == 'crash':
        sound = pygame.mixer.Sound("resource/video game over sound effect.mp3")
    pygame.mixer.Sound.play(sound)


def play_background():
    pygame.mixer.music.load("resource/Theme (30 minutes).mp3")
    pygame.mixer.music.play()


if __name__ == '__main__':
    game = Game()
    game.menu()
