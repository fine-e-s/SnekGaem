import pygame as pg
from pathlib import Path


TILE_SIZE = 100
GAME_WINDOW_SIZE = TILE_SIZE * 10
FULL_WINDOW_SIZE = {'x': GAME_WINDOW_SIZE + TILE_SIZE * 5, 'y': GAME_WINDOW_SIZE}
SCREEN = pg.display.set_mode(list(FULL_WINDOW_SIZE.values()))
FONT_SCALE = 0.8
FONT_SIZE = TILE_SIZE * FONT_SCALE

SNAKE_SKIN = 1
FOOD_SKIN = 1
SNAKE_PATH = Path('assets/snake_skins/')
FOOD_PATH = Path('assets/food_skins/')
CURRENT_SNAKE_PATH = SNAKE_PATH / f'{SNAKE_SKIN}'
CURRENT_FOOD_PATH = FOOD_PATH / f'{FOOD_SKIN}'
FONT = 'assets/04B_30__.TTF'


def snake_cycle():
    global SNAKE_SKIN
    global CURRENT_SNAKE_PATH
    snake_skins_num = len([folder for folder in SNAKE_PATH.iterdir() if folder.is_dir()])
    if SNAKE_SKIN > snake_skins_num:
        SNAKE_SKIN = 1
    elif SNAKE_SKIN < 1:
        SNAKE_SKIN = snake_skins_num
    CURRENT_SNAKE_PATH = SNAKE_PATH / f'{SNAKE_SKIN}'


def food_cycle():
    global FOOD_SKIN
    global CURRENT_FOOD_PATH
    food_skins_num = len([folder for folder in FOOD_PATH.iterdir() if folder.is_dir()])
    if FOOD_SKIN > food_skins_num:
        FOOD_SKIN = 1
    elif FOOD_SKIN < 1:
        FOOD_SKIN = food_skins_num
    CURRENT_FOOD_PATH = FOOD_PATH / f'{FOOD_SKIN}'


def get_snake_path():
    return CURRENT_SNAKE_PATH


def get_food_path():
    return CURRENT_FOOD_PATH
