import pygame as pg
from random import randrange

vec2 = pg.math.Vector2


class Snake:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.Rect(0, 0, self.game.TILE_SIZE - 2, self.game.TILE_SIZE - 2)
        self.segments = []
        self.segments.append(self.get_random_position())
        self.rect.center = self.segments[0]
        self.direction = vec2(0, 0)
        self.turn = False
        self.step_delay = 200  # ms
        self.time = 0
        self.length = 1

    def check_borders(self):
        if self.rect.left < 0 or self.rect.right > self.game.WINDOW_SIZE or self.rect.top < 0 \
                or self.rect.bottom > self.game.WINDOW_SIZE:
            self.game.new_game()

    def check_body(self):
        if [self.rect.center == segment for segment in self.segments]:
            self.game.new_game()

    def check_food(self):
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            self.length += 1

    def control(self, event):
        if event.type == pg.KEYDOWN and self.turn is False:
            if event.key == pg.K_UP and self.direction != vec2(0, self.size):
                self.direction = vec2(0, -self.size)
                self.turn = True
            if event.key == pg.K_DOWN and self.direction != vec2(0, -self.size):
                self.direction = vec2(0, self.size)
                self.turn = True
            if event.key == pg.K_LEFT and self.direction != vec2(self.size, 0):
                self.direction = vec2(-self.size, 0)
                self.turn = True
            if event.key == pg.K_RIGHT and self.direction != vec2(-self.size, 0):
                self.direction = vec2(self.size, 0)
                self.turn = True

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            self.turn = False
            return True
        return False

    def get_random_position(self):
        return [randrange(self.size // 2, self.game.WINDOW_SIZE, self.size),
                randrange(self.size // 2, self.game.WINDOW_SIZE, self.size)]

    def move(self):
        if self.delta_time():
            self.rect.move_ip(self.direction)
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.length:]

    def update(self):
        self.check_borders()
        self.check_body()
        self.check_food()
        self.move()

    def draw(self):
        [pg.draw.rect(self.game.screen, 'green', segment) for segment in self.segments]


class Food:
    def __init__(self, game):
        self.game = game
        self.size = game.TILE_SIZE
        self.rect = pg.Rect(0, 0, self.game.TILE_SIZE - 2, self.game.TILE_SIZE - 2)
        self.rect.center = self.game.snake.get_random_position()

    def draw(self):
        pg.draw.rect(self.game.screen, 'red', self.rect)
