import pygame as pg
WINDOW_TITLE = "snake game"
WINDOW_SIZE = [800, 800]
PLAY_WINDOW_SIZE = [500, 500]
BLANKS_TOP, BLANKS_SIDE = (WINDOW_SIZE[1] - PLAY_WINDOW_SIZE[1]) // 2, (WINDOW_SIZE[0] - PLAY_WINDOW_SIZE[0]) // 2
PIXEL_SIZE = [15, 15]
SCORE_BOARD_HEIGHT = 100

# colors
RED = [225, 0, 0]
WHITE = [225, 225, 225]
BLACK = [0, 0, 0]
BLUE = [0, 0, 225]
GREEN = [0, 225, 225]

# etc

VELOCITY = 15
BAIT_RADIUS = 20
DIRECTIONS = ["n", "e", "s", "w"]
OPPOSITES = {
        "n": "s",
        "s": "n",
        "e": "w",
        "w": "e",
    }

key_to_direction = {
    pg.K_UP: DIRECTIONS[0],
    pg.K_RIGHT: DIRECTIONS[1],
    pg.K_LEFT: DIRECTIONS[3],
    pg.K_DOWN: DIRECTIONS[2],
    pg.K_w: DIRECTIONS[0],
    pg.K_d: DIRECTIONS[1],
    pg.K_s: DIRECTIONS[2],
    pg.K_a: DIRECTIONS[3],
}