from src.values import *
import random
from src.include import *

pg.init()


class SnakeWindow:

    def __init__(self, w_size, background_color):
        self.w_size = w_size
        self.background_color = background_color


class Snake:

    def __init__(self, snake_head, sgl):
        self.snake_head = snake_head
        self.sgl = list(sgl)

    def show_info(self):
        # position, children
        snake_head = self.snake_head
        segments = self.sgl
        print(f"Current position : {snake_head.current_position}")
        print(f"Current direction : {snake_head.current_direction}")
        print(f"Current children are {segments}")
        for seg in segments:
            print(f"{seg.current_position}")

    def render_snake(self, window):
        self.snake_head.draw_head(window)
        for ss in self.sgl:
            ss.show(window)

    def add_child(self):
        if len(self.sgl) == 0:
            self.sgl.append(segment(mother=self.snake_head, color=random_color()))
            self.snake_head.child = self.sgl[0]
            return
        new_segment = segment(color=random_color())
        new_segment.mother = self.sgl[-1]
        self.sgl[-1].child = new_segment
        self.sgl.append(new_segment)

    def pass_to_child(self):
        if len(self.sgl) == 0:
            return
        snake_head = self.sgl[-1]
        while snake_head.mother:
            snake_head.current_position = snake_head.mother.current_position
            snake_head = snake_head.mother

    def get_number_of_segments(self):
        return len(self.sgl)


class Game:
    timer_helper = 0

    def __init__(self, main_window, window, snake, score, timer, score_board, rendered_bait=None):

        self.score = score
        self.window = window
        self.snake = snake
        self.rendered_bait = rendered_bait
        self.main_window = main_window
        self.score_board = score_board
        self.timer = timer

    def throw_bait(self):
        self.rendered_bait = bait(
            position=[random.randint(BAIT_RADIUS, PLAY_WINDOW_SIZE[0] - BAIT_RADIUS),
                      random.randint(BAIT_RADIUS, PLAY_WINDOW_SIZE[1] - BAIT_RADIUS)],
            bait_timer=100,
        )
        self.rendered_bait.render_bait(self.main_window)

    def show_bait(self):
        positions = set_relative(self.rendered_bait.position)
        return pg.draw.rect(self.main_window, RED, [positions[0], positions[1], BAIT_RADIUS, BAIT_RADIUS])

    def check_bait_timeout(self):
        if self.rendered_bait:
            self.show_bait()
            if self.rendered_bait.bait_timer < 0:
                self.rendered_bait = None
            else:
                self.rendered_bait.bait_timer -= 1

    def update_timer(self):
        self.timer_helper += 1
        if self.timer_helper == 10:
            self.timer_helper = 0
            self.timer += 1

    def check_collision(self):
        # bait has an enclosed-self space
        # we check if the head has by-passed the space
        game_snake = self.snake.snake_head
        bait_pos_limit = [
            [self.rendered_bait.position[0], self.rendered_bait.position[1]],
            [self.rendered_bait.position[0] + BAIT_RADIUS, self.rendered_bait.position[1]],
            [self.rendered_bait.position[0], self.rendered_bait.position[1] + BAIT_RADIUS],
            [self.rendered_bait.position[0] + BAIT_RADIUS, self.rendered_bait.position[1] + BAIT_RADIUS],
        ]
        snake_pos_limits = [
            [game_snake.current_position[0], game_snake.current_position[1]],
            [game_snake.current_position[0] + PIXEL_SIZE[0], game_snake.current_position[1]],
            [game_snake.current_position[0], game_snake.current_position[1] + PIXEL_SIZE[0]],
            [game_snake.current_position[0] + PIXEL_SIZE[0], game_snake.current_position[1] + PIXEL_SIZE[0]]

        ]

        return is_within(bait_pos_limit, snake_pos_limits, game_snake.current_direction)

    def self_collision(self):
        game_snake = self.snake.snake_head
        if len(self.snake.sgl) <= 4:
            return False
        for i in range(4, len(self.snake.sgl)):
            if self.snake.sgl[i].current_position == game_snake.current_position:
                print(f"Segment position is {self.snake.sgl[i].current_position}\tHead position is {game_snake.current_position}")
                self.reset_score()
                return True
        return False

    def game_over(self):
        pass

    def reset_score(self):
        self.score = 0
        self.timer = 0
        self.timer_helper = 0
        self.snake.sgl = []
        self.rendered_bait = None
        self.throw_bait()
        print("Game over")
        return

    def add_score(self):
        self.self_collision()
        if self.check_collision():
            self.score += 1
            self.rendered_bait = None
            self.snake.add_child()
            print(f"Score is {self.score}")

    def bait_exists(self):
        if not self.rendered_bait:
            self.throw_bait()

    def main_game_loop(self):
        game_snake = self.snake
        main_window = self.main_window
        game_snake.render_snake(main_window)
        # game_snake.show_info()
        self.bait_exists()
        self.add_score()
        self.check_bait_timeout()

    def setup(self):
        pg.time.delay(100)
        self.main_window.fill(WHITE)
        self.update_timer()
        self.score_board.update(self.score, self.timer)
        show_boundaries(self.main_window)
        self.score_board.render_board(self.main_window)
        self.main_game_loop()


class ScoreBoard:

    def __init__(self, score=None, timer=None):
        self.score = score
        self.timer = timer

    def add_score(self):
        self.score += 1

    def update(self, score, time):
        self.score = score
        self.timer = time

    def render_board(self, window):
        font_used = pg.font.Font('freesansbold.ttf', 32)
        string = str(self.timer // 60) + " : " + str(self.timer % 60) + "   " + "Score : " + str(self.score)
        rendered_text = font_used.render(string, False, BLACK, WHITE)
        text_rect = rendered_text.get_rect()
        text_placement_info = set_placement()
        text_rect.center = text_placement_info[-1]

        window.blit(rendered_text, text_rect)


class segment:
    def __init__(self, color,  mother=None, child=None, current_position=None, current_direction=None):
        self.color = color
        self.mother = mother
        self.child = child
        self.current_position = current_position
        self.current_direction = current_direction

    def show(self, window):
        relative_position = set_relative(self.current_position)
        return pg.draw.rect(window, self.color, [relative_position[0], relative_position[1], PIXEL_SIZE[0],
                                                 PIXEL_SIZE[1]])

    def pass_info(self):
        self.child.current_position = self.current_position
        print(f"Me is {self}\tMother is {self.mother}\t Child is {self.child}")
        print(f" me position is {self.current_position}\tChild position is {self.child.current_position}\n\n")


class head(segment):

    def __init__(self, size, current_position, win, current_direction, previous_direction, color):
        super().__init__(color=color)
        self.size = size
        self.current_position = current_position
        self.win = win
        self.current_direction = str(current_direction)
        self.previous_direction = str(previous_direction)

    def draw_head(self, window):
        self.position_checks()
        relative_position = set_relative(self.current_position)
        return pg.draw.rect(window, self.color, [relative_position[0],
                                            relative_position[1],
                                            self.size[0],
                                            self.size[1]])

    def position_checks(self):
        if self.current_position[0] < 0:
            self.current_position[0] = self.win.w_size[0] - PIXEL_SIZE[0]
        elif self.current_position[0] > self.win.w_size[0] - PIXEL_SIZE[0]:
            self.current_position[0] = 0
        if self.current_position[1] > self.win.w_size[1] - PIXEL_SIZE[1]:
            self.current_position[1] = 0
        elif self.current_position[1] < 0:
            self.current_position[1] = self.win.w_size[1] - PIXEL_SIZE[1]


class bait:

    def __init__(self, position, bait_timer):
        self.position = position
        self.bait_timer = bait_timer

    def render_bait(self, main_window):
        self.bait_timer = 100
        positions = set_relative(self.position)
        return pg.draw.rect(main_window, RED, [positions[0], positions[1], BAIT_RADIUS, BAIT_RADIUS])


def main():

    game_running = True
    game_window = SnakeWindow(
        w_size=PLAY_WINDOW_SIZE,
        background_color=WHITE,
    )

    main_window = pg.display.set_mode(WINDOW_SIZE)
    spawn_point = [WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2]
    game_snake = Snake(
        snake_head=head(
            PIXEL_SIZE,
            spawn_point,
            win=game_window,
            current_direction="e",
            previous_direction="n",
            color=random_color()
        ),
        sgl=[],
    )
    game = Game(
        main_window=main_window,
        window=game_window,
        snake=game_snake,
        score=0,
        timer=0,
        score_board=ScoreBoard()
    )

    snake_head = game_snake.snake_head

    pg.display.set_caption(WINDOW_TITLE)
    while game_running:
        game.setup()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_running = False

        res = event_listener(snake_head.current_direction, snake_head.current_position)
        game_snake.pass_to_child()
        res[0] = snake_head.current_position
        if valid_direction_change(direction=res[1],
                                  current_direction=snake_head.current_direction,
                                  snake_head_only=game_snake.get_number_of_segments() == 0):
            snake_head.previous_direction = snake_head.current_direction
            snake_head.current_direction = res[1]
        else:
            snake_head.current_position = map_direction_change(snake_head.current_direction,
                                                               snake_head.current_position)
        pg.display.update()


if __name__ == '__main__':
    main()
