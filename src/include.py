from src.values import *
import pygame as pg
from random import randrange


def random_color():
    return [randrange(0, 225), randrange(0, 225), randrange(0, 225)]


def set_relative(point):
    x, y = point[0], point[1]
    x += BLANKS_TOP
    y += BLANKS_SIDE
    return [x, y]


def draw_line(window, starting_point, end_point):
    return pg.draw.line(window, BLACK, starting_point, end_point)


def show_boundaries(game_window=None):
    # the window should be centered
    vertices = [
        [BLANKS_TOP, BLANKS_SIDE],
        [BLANKS_TOP + PLAY_WINDOW_SIZE[0], BLANKS_SIDE],
        [BLANKS_TOP, BLANKS_SIDE + PLAY_WINDOW_SIZE[1]],
        [BLANKS_TOP + PLAY_WINDOW_SIZE[0], PLAY_WINDOW_SIZE[1] + BLANKS_SIDE]
    ]
    points = [[0, 1], [0, 2], [3, 1], [3, 2]]
    for point in points:
        draw_line(game_window, vertices[point[0]], vertices[point[1]])


def event_listener(current_direction, current_position):

    keys_entry, temp = [], current_position

    keys_pressed = pg.key.get_pressed()
    for key in key_to_direction.keys():
        if keys_pressed[key]:
            keys_entry.append(key_to_direction.get(key))
    if len(keys_entry) == 0:
        return [map_direction_change(current_direction, current_position), current_direction]
    for key_press in keys_entry:
        if not direction_directly_opposite(key_press, current_direction):
            temp = map_direction_change(key_press, temp)
        return [temp, keys_entry[0]]


def map_direction_change(direction, current_position):
    if direction == DIRECTIONS[0]:
        return [current_position[0], current_position[1] - VELOCITY]
    elif direction == DIRECTIONS[1]:
        return [current_position[0] + VELOCITY, current_position[1]]
    elif direction == DIRECTIONS[2]:
        return [current_position[0], current_position[1] + VELOCITY]
    elif direction == DIRECTIONS[3]:
        return [current_position[0] - VELOCITY, current_position[1]]


def is_within(bait_points, snake_points, direction):
    if direction == "n":
        if bait_points[0][0] <= snake_points[2][0] <= bait_points[1][0] or bait_points[0][0] <= snake_points[3][0] <= bait_points[1][0]:
            if snake_points[0][1] <= bait_points[2][1]:
                return True
    elif direction == "e":
        if bait_points[0][1] <= snake_points[0][1] <= bait_points[2][1] or bait_points[0][1] <= snake_points[2][1] <= bait_points[2][1]:
            if snake_points[1][0] >= bait_points[0][0]:
                return True
    elif direction == "s":
        if bait_points[0][0] <= snake_points[2][0] <= bait_points[1][0] or bait_points[0][0] <= snake_points[3][0] <= bait_points[1][0]:
            if snake_points[2][1] >= bait_points[0][1]:
                return True
    elif direction == "w":
        if bait_points[0][1] <= snake_points[0][1] <= bait_points[2][1] or bait_points[0][1] <= snake_points[2][1] <= bait_points[2][1]:
            if snake_points[0][0] <= bait_points[1][0]:
                return True
    return False


def valid_direction_change(direction, current_direction, snake_head_only=False):
    if snake_head_only and direction != current_direction:
        return True
    elif direction != current_direction and not direction_directly_opposite(direction, current_direction):
        return True
    return False


def direction_directly_opposite(direction, current_direction):
    if direction == OPPOSITES.get(current_direction):
        return True
    return False


def set_placement():

    # left_top, right_top, bottom_left, bottom_right, center

    # 100 from top
    _y_offset = 50
    _x_offset, width = (WINDOW_SIZE[0] - PLAY_WINDOW_SIZE[0]) // 2, PLAY_WINDOW_SIZE[0]
    return_points = [[_x_offset, _y_offset],
                     [_x_offset + width, _y_offset],
                     [_x_offset, _y_offset + SCORE_BOARD_HEIGHT],
                     [_x_offset + width, _y_offset + SCORE_BOARD_HEIGHT]
                     ]
    centre = [_x_offset + width // 2, _y_offset + SCORE_BOARD_HEIGHT // 2]
    return_points.append(centre)

    return return_points













