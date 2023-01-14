import pygame as pg

import highscores
import settings
from settings import *
import sys
import os


class Menu:
    def __init__(self, game):
        self.game = game

        SCREEN.fill('black')
        self.playing = self.game.playing

        self.buttons = []
        self.other_text = []
        self.button_index = 0

        self.cursor_rect = pg.Rect(0, 0, 0, 0)
        self.offset = -FONT_SIZE / 2

        self.state = ''

        main_menu = MainMenu(self)

    def run(self):
        while not self.playing:
            self.update()

    def control(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP or event.key == pg.K_LEFT:
                if (self.buttons[self.button_index]['text'] == f'Snake skin <{settings.SNAKE_SKIN}>' or
                    self.buttons[self.button_index]['text'] == f'Food skin <{settings.FOOD_SKIN}>') \
                        and event.key == pg.K_LEFT:
                    self.buttons[self.button_index]['action'](-1)
                else:
                    self.button_index -= 1
                    self.index_cycle()
            if event.key == pg.K_DOWN or event.key == pg.K_RIGHT:
                if (self.buttons[self.button_index]['text'] == f'Snake skin <{settings.SNAKE_SKIN}>' or
                    self.buttons[self.button_index]['text'] == f'Food skin <{settings.FOOD_SKIN}>') \
                        and event.key == pg.K_RIGHT:
                    self.buttons[self.button_index]['action'](1)
                else:
                    self.button_index += 1
                    self.index_cycle()
            if event.key == pg.K_RETURN:
                if not (self.buttons[self.button_index]['text'] == f'Snake skin <{settings.SNAKE_SKIN}>' or
                        self.buttons[self.button_index]['text'] == f'Food skin <{settings.FOOD_SKIN}>'):
                    self.buttons[self.button_index]['action']()
            if event.key == pg.K_ESCAPE:
                if self.state != 'MainMenu':
                    self.back_to_main()
                else:
                    self.exit()
            if self.state == 'Highscore_submitting' and self.button_index == 0:
                self.buttons[self.button_index]['enter'](event)

    def index_cycle(self):
        self.button_index = self.button_index % len(self.buttons)

    def update(self):
        SCREEN.fill('black')
        if self.state == 'MainMenu':
            self.draw_logo()
        self.draw_preview()
        self.draw_other_text()
        self.draw_buttons()
        self.draw_cursor()
        pg.display.flip()
        self.game.check_event()

    def get_buttons(self, buttons):
        self.buttons = buttons

    def draw_logo(self):
        self.game.draw_text('/ SNEK /', FONT_SIZE * 2, FULL_WINDOW_SIZE['x'] / 2, FULL_WINDOW_SIZE['y'] / 3)

    def draw_buttons(self):
        for button in self.buttons:
            left = self.game.draw_text(button['text'], FONT_SIZE, button['x'], button['y'])
            button.update({'left': left})

    def draw_cursor(self):
        self.cursor_rect.center = (self.buttons[self.button_index]['left'],
                                   self.buttons[self.button_index]['y'] + FONT_SIZE / 6)
        self.game.draw_text('*', FONT_SIZE, self.cursor_rect.centerx + self.offset, self.cursor_rect.centery)

    def draw_preview(self):
        if self.state == 'Options':
            self.game.sprite_group.draw(SCREEN)

    def get_other_text(self, strings):
        self.other_text = strings

    def draw_other_text(self):
        for string in self.other_text:
            self.game.draw_text(*string)

    def back_to_main(self):
        if self.state == 'Options':
            self.button_index = 2
        elif self.state == 'Highscores':
            self.button_index = 1
        else:
            self.button_index = 0

        self.other_text = []

        main_menu = MainMenu(self)

    def exit(self):
        pg.quit()
        sys.exit()


class MainMenu:
    def __init__(self, menu):
        self.menu = menu

        self.menu.state = 'MainMenu'

        self.buttons = {}
        self.create_buttons()
        self.arrange_buttons(FULL_WINDOW_SIZE['x'] / 2, FULL_WINDOW_SIZE['y'] * 0.8)
        self.menu.get_buttons(self.buttons)

    def create_buttons(self):
        self.buttons = [
            {'text': 'Start Game', 'x': 0, 'y': 0, 'action': self.start},
            {'text': 'Highscores', 'x': 0, 'y': 0, 'action': self.open_highscores},
            {'text': 'Options', 'x': 0, 'y': 0, 'action': self.open_options},
            {'text': 'Exit', 'x': 0, 'y': 0, 'action': self.menu.exit}
        ]

    def arrange_buttons(self, x_offset, y_offset):
        for button in self.buttons:
            x = x_offset
            y = y_offset + (
                    -(len(self.buttons) / 2) * FONT_SIZE +
                    (self.buttons.index(button) * FONT_SIZE)
            )
            button.update({'x': x, 'y': y})

    def start(self):
        self.menu.game.run()

    def open_highscores(self):
        highscores = Highscores(self.menu)

    def open_options(self):
        options = Options(self.menu)


class Options:
    def __init__(self, menu):
        self.menu = menu

        self.menu.state = 'Options'

        self.menu.button_index = 0
        self.buttons = {}
        self.create_buttons()
        self.create_preview()

    def create_buttons(self):
        self.buttons = [
            {'text': f'Snake skin <{settings.SNAKE_SKIN}>', 'x': 0, 'y': 0, 'action': self.change_snake},
            {'text': f'Food skin <{settings.FOOD_SKIN}>', 'x': 0, 'y': 0, 'action': self.change_food},
            {'text': 'Reset highscores', 'x': 0, 'y': 0, 'action': self.reset_highscores},
            {'text': 'Back', 'x': 0, 'y': 0, 'action': self.menu.back_to_main}
        ]
        self.arrange_buttons(FULL_WINDOW_SIZE['x'] / 2, FULL_WINDOW_SIZE['y'] * 0.8)
        self.menu.get_buttons(self.buttons)

    def arrange_buttons(self, x_offset, y_offset):
        for button in self.buttons:
            x = x_offset
            y = y_offset + (
                    -(len(self.buttons) / 2) * FONT_SIZE +
                    (self.buttons.index(button) * FONT_SIZE)
            )
            button.update({'x': x, 'y': y})

    def change_snake(self, x):
        settings.SNAKE_SKIN += x
        snake_cycle()
        self.create_buttons()
        self.create_preview()

    def change_food(self, x):
        settings.FOOD_SKIN += x
        food_cycle()
        self.create_buttons()
        self.create_preview()

    def create_preview(self):
        self.menu.game.sprite_group.empty()
        snake_pos = {'x': FULL_WINDOW_SIZE['x'] / 3, 'y': FULL_WINDOW_SIZE['y'] / 3}
        food_pos = (FULL_WINDOW_SIZE['x'] - snake_pos['x'] + TILE_SIZE, snake_pos['y'])
        preview_size = TILE_SIZE * 2
        preview_images = [
            {'name': 'Head.png', 'location': get_snake_path,
             'pos': (snake_pos['x'] - preview_size / 2, snake_pos['y'] - preview_size / 2),
             'rotation': 0, 'scale': preview_size},
            {'name': 'Curved.png', 'location': get_snake_path,
             'pos': (snake_pos['x'] + preview_size / 2, snake_pos['y'] - preview_size / 2),
             'rotation': 270, 'scale': preview_size},
            {'name': 'Curved.png', 'location': get_snake_path,
             'pos': (snake_pos['x'] + preview_size / 2, snake_pos['y'] + preview_size / 2),
             'rotation': 180, 'scale': preview_size},
            {'name': 'Tail.png', 'location': get_snake_path,
             'pos': (snake_pos['x'] - preview_size / 2, snake_pos['y'] + preview_size / 2),
             'rotation': 180, 'scale': preview_size},
            {'name': 'Food.png', 'location': get_food_path,
             'pos': food_pos,
             'rotation': 0, 'scale': preview_size * 2}
        ]
        for item in preview_images:
            preview_sprite = pg.sprite.Sprite(self.menu.game.sprite_group)
            name = item['name']
            preview_sprite.image = pg.image.load(os.path.join(item['location'](), name))
            preview_sprite.image = pg.transform.scale(preview_sprite.image, [item['scale']] * 2)
            preview_sprite.image = pg.transform.rotate(preview_sprite.image, item['rotation'])
            preview_sprite.rect = preview_sprite.image.get_rect()
            preview_sprite.rect.center = item['pos']

    def reset_highscores(self):
        self.menu.game.highscores.reset()


class Highscores:
    def __init__(self, menu):
        self.menu = menu

        self.menu.state = 'Highscores'

        self.menu.button_index = 0
        self.buttons = [
            {'text': 'Back', 'x': FULL_WINDOW_SIZE['x'] / 2, 'y': FULL_WINDOW_SIZE['y'] - FONT_SIZE,
             'action': self.menu.back_to_main}]
        self.other_text = []
        self.create_highscores()
        self.menu.get_buttons(self.buttons)
        self.menu.get_other_text(self.other_text)

    def create_highscores(self):
        score_list = self.menu.game.highscores.highscores_list
        for entry in score_list:
            self.other_text.append([entry['name'], FONT_SIZE, FULL_WINDOW_SIZE['x'] / 2,
                                   score_list.index(entry) * FONT_SIZE + FULL_WINDOW_SIZE['y'] * 0.1])
            self.other_text.append([entry['place'], FONT_SIZE, FULL_WINDOW_SIZE['x'] / 2 - TILE_SIZE * 5,
                                   score_list.index(entry) * FONT_SIZE + FULL_WINDOW_SIZE['y'] * 0.1])
            self.other_text.append([str(entry['score']), FONT_SIZE, FULL_WINDOW_SIZE['x'] / 2 + TILE_SIZE * 5,
                                   score_list.index(entry) * FONT_SIZE + FULL_WINDOW_SIZE['y'] * 0.1])


class HighscoreSubmitting:
    def __init__(self, menu, score, place):
        self.menu = menu
        self.menu.game.playing = False
        self.score = score
        self.place = place

        self.menu.state = 'Highscore_submitting'

        self.menu.button_index = 0
        self.buttons = []
        self.other_text = [[f'SCORE:{self.score}', FONT_SIZE, FULL_WINDOW_SIZE['x'] / 2, FULL_WINDOW_SIZE['y'] * 0.1],
                           ['Enter your name:', FONT_SIZE, FULL_WINDOW_SIZE['x'] / 2,
                            FULL_WINDOW_SIZE['y'] * 0.1 + FONT_SIZE]]
        self.menu.get_other_text(self.other_text)
        self.name = ''
        self.time = highscores.get_current_time()
        self.create_highscore_entry()

    def create_highscore_entry(self):
        self.buttons = [
            {'text': self.name, 'x': FULL_WINDOW_SIZE['x'] / 2, 'y': FULL_WINDOW_SIZE['y'] / 2,
             'action': lambda: None, 'enter': self.enter_char},
            {'text': 'Enter', 'x': FULL_WINDOW_SIZE['x'] / 2, 'y': FULL_WINDOW_SIZE['y'] - FONT_SIZE,
             'action': self.submit_highscore}
        ]
        self.menu.get_buttons(self.buttons)

    def submit_highscore(self):
        if len(self.name) >= 1:
            score_list = self.menu.game.highscores.highscores_list
            score_list.append({'place': f'{self.place}', 'name': f'{self.name}', 'score': self.score,
                               'time': self.time})
            score_list = sorted(sorted(
                score_list, key=lambda d: d['time'], reverse=True),
                key=lambda e: e['score'], reverse=True
            )
            score_list = score_list[:10]
            for place, entry in enumerate(score_list):
                entry.update({'place': str(place + 1)})
            self.menu.game.highscores.highscores_list = score_list
            self.menu.game.highscores.write_file()
            self.menu.back_to_main()
            self.menu.game.run()

    def enter_char(self, event):
        print(event.key)
        if event.key not in [pg.K_BACKSPACE, pg.K_RETURN, pg.KSCAN_RETURN, 1073741912, 9, 32, 50, 51, 52, 55] and \
                len(self.name) < 14:
            self.name += event.unicode
        if event.key == pg.K_BACKSPACE:
            self.name = self.name[:-1]
        self.create_highscore_entry()
