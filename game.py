import pygame as pg

import settings
from settings import *
from highscores import Highscores
from menu import Menu
from game_objects import Snake, Food
import sys


class Game:
    def __init__(self):
        pg.init()

        self.sprite_group = pg.sprite.Group()
        self.clock = pg.time.Clock()

        self.playing = False
        self.pause = False
        self.highscores = Highscores()
        self.menu = Menu(self)
        self.menu.run()

    def draw_grid(self):
        width = 1
        [pg.draw.line(SCREEN, [50] * 3, (x, 0), (x, GAME_WINDOW_SIZE), width)
         for x in range(0, GAME_WINDOW_SIZE + 1, TILE_SIZE)]
        [pg.draw.line(SCREEN, [50] * 3, (0, y), (GAME_WINDOW_SIZE, y), width)
         for y in range(0, GAME_WINDOW_SIZE, TILE_SIZE)]

    def new_game(self):
        self.sprite_group.empty()
        self.snake = Snake(self)
        self.food = Food(self)

    def update(self):
        if not self.pause:
            self.snake.update()
        pg.display.flip()
        self.clock.tick(60)

    def draw(self):
        self.sprite_group.empty()
        SCREEN.fill('black')
        # if self.playing:
        self.draw_grid()
        self.draw_score()
        self.snake.draw()
        self.food.draw()

        self.sprite_group.draw(SCREEN)

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if self.playing:
                self.snake.control(event)

            if not self.playing:
                self.menu.control(event)

    def run(self):
        self.playing = True
        self.new_game()
        while self.playing:
            self.check_event()
            self.update()
            self.draw()

    def draw_text(self, text, size, x, y):
        size = round(size / 1.3)
        font = pg.font.Font(FONT, size)
        text_surface = font.render(text, False, [255] * 3)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        SCREEN.blit(text_surface, text_rect)
        return text_rect.left

    def draw_score(self):
        score = (self.snake.length - 1) * self.snake.length * 10
        self.draw_text('SCORE:', FONT_SIZE, FULL_WINDOW_SIZE['x'] - (FULL_WINDOW_SIZE['x'] - GAME_WINDOW_SIZE) / 2,
                       FULL_WINDOW_SIZE['y'] * 0.1)
        self.draw_text(str(score), FONT_SIZE, FULL_WINDOW_SIZE['x'] - (FULL_WINDOW_SIZE['x'] - GAME_WINDOW_SIZE) / 2,
                       FULL_WINDOW_SIZE['y'] * 0.1 + FONT_SIZE)

        self.draw_text('P - pause', FONT_SIZE / 2, FULL_WINDOW_SIZE['x'] - (FULL_WINDOW_SIZE['x'] - GAME_WINDOW_SIZE) / 2,
                       FULL_WINDOW_SIZE['y'] * 0.9 - FONT_SIZE / 2)
        self.draw_text('ESC - main menu', FONT_SIZE / 2,
                       FULL_WINDOW_SIZE['x'] - (FULL_WINDOW_SIZE['x'] - GAME_WINDOW_SIZE) / 2,
                       FULL_WINDOW_SIZE['y'] * 0.9)

