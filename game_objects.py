import pygame as pg

import highscores
import menu
from settings import *
from random import randrange
import os

vec2 = pg.math.Vector2


class Snake:
    def __init__(self, game):
        self.game = game

        self.rect = pg.Rect(0, 0, TILE_SIZE - 9, TILE_SIZE - 9)

        self.length = 1
        self.rect.center = self.get_random_position()
        self.segments = []
        self.segments.append(self.rect)

        self.grow = False

        self.direction = vec2(0, 0)
        self.head_direction = 'Left'
        self.turn = False

        self.step_delay = 200  # ms
        self.time = 0

    def check_borders(self):
        if self.rect.left < 0 or self.rect.right > GAME_WINDOW_SIZE or self.rect.top < 0 \
                or self.rect.bottom > GAME_WINDOW_SIZE:
            self.check_highscore()
            self.game.new_game()

    def check_body(self):
        for x in range(0, self.length - 1):
            if self.rect.center == self.segments[x].center:
                self.check_highscore()
                self.game.new_game()

    def check_highscore(self):
        score = (self.length - 1) * self.length * 10
        if score > 0:
            score_list = highscores.get_file()
            for entry in score_list[::-1]:
                if entry['score'] <= score:
                    highscore_entry = menu.HighscoreSubmitting(self.game.menu, score)

    def check_food(self):
        if self.rect.center == self.game.food.rect.center:
            self.game.food.rect.center = self.get_random_position()
            self.grow = True
            while self.game.food.rect.center in [segment.center for segment in self.segments]:
                self.game.food.rect.center = self.get_random_position()

    def control(self, event):
        if event.type == pg.KEYDOWN and self.turn is False:
            if not self.game.pause:
                if event.key == pg.K_UP and self.direction != vec2(0, TILE_SIZE):
                    self.direction = vec2(0, -TILE_SIZE)
                    self.turn = True
                if event.key == pg.K_DOWN and self.direction != vec2(0, -TILE_SIZE):
                    self.direction = vec2(0, TILE_SIZE)
                    self.turn = True
                if event.key == pg.K_LEFT and self.direction != vec2(TILE_SIZE, 0):
                    self.direction = vec2(-TILE_SIZE, 0)
                    self.turn = True
                if event.key == pg.K_RIGHT and self.direction != vec2(-TILE_SIZE, 0):
                    self.direction = vec2(TILE_SIZE, 0)
                    self.turn = True
                if event.key == pg.K_ESCAPE:
                    self.game.playing = False
                    self.game.menu.run()
            if event.key == pg.K_p:
                self.game.pause = not self.game.pause

    def delta_time(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time > self.step_delay:
            self.time = time_now
            self.turn = False
            return True
        return False

    def get_random_position(self):
        return [randrange(TILE_SIZE // 2, GAME_WINDOW_SIZE, TILE_SIZE),
                randrange(TILE_SIZE // 2, GAME_WINDOW_SIZE, TILE_SIZE)]

    def set_head_direction(self):
        if self.direction == [0, -TILE_SIZE]:
            return 'Up'
        elif self.direction == [0, TILE_SIZE]:
            return 'Down'
        elif self.direction == [TILE_SIZE, 0]:
            return 'Right'
        elif self.direction == [-TILE_SIZE, 0]:
            return 'Left'
        else:
            return 'Left'

    def move(self):
        if self.delta_time():
            if self.grow:
                self.length += 1
                self.grow = False
            self.rect.move_ip(self.direction)
            self.head_direction = self.set_head_direction()
            self.segments.append(self.rect.copy())
            self.segments = self.segments[-self.length:]

    def update(self):
        self.check_food()
        self.move()
        self.check_borders()
        self.check_body()

    def draw(self):
        self.game.sprite_group.add(Block(self.game, self.segments[len(self.segments) - 1].center,
                                         len(self.segments) - 1, 'Snake'))
        if self.length > 1:
            for x in range(0, len(self.segments) - 1):
                self.game.sprite_group.add(Block(self.game, self.segments[x].center, x, 'Snake'))


class Food:
    def __init__(self, game):
        self.game = game
        self.rect = pg.Rect(0, 0, TILE_SIZE - 20, TILE_SIZE - 20)
        self.rect.center = self.game.snake.get_random_position()

    def draw(self):
        self.game.sprite_group.add(Block(self.game, self.rect.center, 0, 'Food'))


class Block(pg.sprite.Sprite):
    def __init__(self, game, pos, segment_num, block_type):
        self.game = game
        super().__init__(game.sprite_group)
        if block_type == 'Snake':
            image_type = self.set_type(segment_num)
            name = image_type + '.png'
            self.image = pg.image.load(os.path.join(get_snake_path(), name))
            self.image = pg.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            if image_type == 'Curved':
                self.image = pg.transform.rotate(self.image, self.check_turn(segment_num)[1])
            else:
                self.image = pg.transform.rotate(self.image, self.check_direction(segment_num)[1])
            self.rect = self.image.get_rect()
            self.rect.center = pos
        elif block_type == 'Food':
            name = 'Food.png'
            self.image = pg.image.load(os.path.join(get_food_path(), name))
            self.image = pg.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            self.rect = self.image.get_rect()
            self.rect.center = pos

    def set_type(self, segment_num):
        length = self.game.snake.length
        if segment_num == 0 and length == 1:
            segment_type = 'Head-Single'
        elif segment_num == length - 1:
            segment_type = 'Head'
        elif segment_num == 0:
            segment_type = 'Tail'
        elif self.check_turn(segment_num)[0]:
            segment_type = 'Curved'
        else:
            segment_type = 'Straight-Body'
        return segment_type

    def check_direction(self, segment_num):
        head_direction = self.game.snake.head_direction

        up = 'Up', 270
        down = 'Down', 90
        right = 'Right', 180
        left = 'Left', 0

        # head is last in list
        # tail is first

        if segment_num == len(self.game.snake.segments) - 1 or (segment_num == 0 and len(self.game.snake.segments) < 3):
            if head_direction == 'Up':
                return up
            elif head_direction == 'Down':
                return down
            elif head_direction == 'Right':
                return right
            elif head_direction == 'Left':
                return left

        elif 0 < segment_num < len(self.game.snake.segments) - 1:
            cur_seg = self.game.snake.segments[segment_num]
            next_seg = self.game.snake.segments[segment_num - 1]

            if cur_seg.centerx == next_seg.centerx:
                if cur_seg.centery < next_seg.centery:
                    return up
                else:
                    return down
            if cur_seg.centery == next_seg.centery:
                if cur_seg.centerx < next_seg.centerx:
                    return left
                else:
                    return right

        elif segment_num == 0:
            cur_seg = self.game.snake.segments[segment_num]
            prev_seg = self.game.snake.segments[segment_num + 1]

            if cur_seg.centerx == prev_seg.centerx:
                if cur_seg.centery < prev_seg.centery:
                    return down
                else:
                    return up
            if cur_seg.centery == prev_seg.centery:
                if cur_seg.centerx < prev_seg.centerx:
                    return right
                else:
                    return left

        else:
            return left

    def check_turn(self, segment_num):
        cur_dir = self.check_direction(segment_num)
        next_dir = self.check_direction(segment_num + 1)
        turn = [False, 0]
        if cur_dir != next_dir:
            if (cur_dir[0] == 'Up' and next_dir[0] == 'Right') or (cur_dir[0] == 'Left' and next_dir[0] == 'Down'):
                turn = [True, 0]
            elif (cur_dir[0] == 'Right' and next_dir[0] == 'Up') or (cur_dir[0] == 'Down' and next_dir[0] == 'Left'):
                turn = [True, 180]
            elif (cur_dir[0] == 'Left' and next_dir[0] == 'Up') or (cur_dir[0] == 'Down' and next_dir[0] == 'Right'):
                turn = [True, 90]
            elif (cur_dir[0] == 'Right' and next_dir[0] == 'Down') or (cur_dir[0] == 'Up' and next_dir[0] == 'Left'):
                turn = [True, 270]
        return turn
