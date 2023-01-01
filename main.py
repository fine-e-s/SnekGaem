import pygame as pg
from game_objects import Snake, Food, Block
import sys


class Game:
    def __init__(self):
        pg.init()
        self.TILE_SIZE = 100
        self.WINDOW_SIZE = self.TILE_SIZE * 10
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.sprite_group = pg.sprite.Group()
        self.clock = pg.time.Clock()
        self.new_game()

    def draw_grid(self):
        width = 1
        h_width = width // 2
        [pg.draw.line(self.screen, [50] * 3, (x, 0), (x, self.WINDOW_SIZE), width)
         for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
        [pg.draw.line(self.screen, [50] * 3, (0, y), (self.WINDOW_SIZE, y), width)
         for y in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]

    def new_game(self):
        self.sprite_group.empty()
        self.snake = Snake(self)
        self.food = Food(self)

    def update(self):
        self.snake.update()
        pg.display.flip()
        self.clock.tick(60)

    def draw(self):
        self.sprite_group.empty()
        self.screen.fill('black')
        self.draw_grid()
        self.snake.draw()
        self.food.draw()

        self.sprite_group.draw(self.screen)

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.snake.control(event)

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
