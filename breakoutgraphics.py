"""
This is a simple brick-our game for python learning
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40  # Height of a brick (in pixels).
BRICK_HEIGHT = 15  # Height of a brick (in pixels).
BRICK_ROWS = 10  # Number of rows of bricks.
BRICK_COLS = 10  # Number of columns of bricks.
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10  # Radius of the ball (in pixels).
PADDLE_WIDTH = 75  # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels).
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7.0  # Initial vertical speed for the ball.
MAX_X_SPEED = 2  # Maximum initial horizontal speed for the ball.


class BreakoutGraphics:
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):

        # Create a graphical window, with some extra space.
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle.
        self.paddle_offset = paddle_offset
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        onmousemoved(self.set_paddle_position)

        # Create a oval in the graphical window.
        self.oval = GOval(ball_radius * 2, ball_radius * 2)
        self.oval.filled = True
        self.oval.fill_color = "navy"

        # draw brick
        for i in range(brick_cols):
            for j in range(brick_rows):
                self.brick = GRect(brick_width, brick_height)
                self.brick.filled = True
                if i * (brick_spacing + brick_height) < 40:
                    self.brick.fill_color = "red"
                    self.window.add(self.brick, j * (brick_spacing + brick_width), i * (brick_spacing + brick_height))
                elif 40 <= i * (brick_spacing + brick_height) < 80:
                    self.brick.fill_color = "orange"
                    self.window.add(self.brick, j * (brick_spacing + brick_width), i * (brick_spacing + brick_height))
                elif 80 <= i * (brick_spacing + brick_height) < 120:
                    self.brick.fill_color = "yellow"
                    self.window.add(self.brick, j * (brick_spacing + brick_width), i * (brick_spacing + brick_height))
                elif 120 <= i * (brick_spacing + brick_height) < 160:
                    self.brick.fill_color = "lightgreen"
                    self.window.add(self.brick, j * (brick_spacing + brick_width), i * (brick_spacing + brick_height))
                elif 160 <= i * (brick_spacing + brick_height) < 200:
                    self.brick.fill_color = "lightblue"
                    self.window.add(self.brick, j * (brick_spacing + brick_width), i * (brick_spacing + brick_height))

        # record for number of bricks
        self.num_brick = brick_rows*brick_cols

        # set oval position
        self.oval_position()
        # if self.ball_y_in_right_zone():
        #     self.oval_position()

        # parameter for animation
        self.click = False
        self.__dx = 0
        self.__dy = 0

        # activate the game while mouse click
        onmouseclicked(self.set_start)
        self.set_oval_velocity()

    def set_paddle_position(self, event):
        self.paddle.x = event.x - self.paddle.width / 2
        if self.paddle.x >= self.window.width - self.paddle.width:
            self.paddle.x = self.window.width - self.paddle.width
        if self.paddle.x + self.paddle.width / 2 <= self.paddle.width / 2:
            self.paddle.x = 0

        self.paddle.y = self.window.height - self.paddle_offset
        self.window.add(self.paddle)

    def oval_position(self):
        self.oval.x = random.randint(0, self.window.width - self.oval.width)
        self.oval.y = random.randint(self.brick.y + 20, self.window.height - (self.oval.height + self.paddle_offset))
        self.window.add(self.oval, self.oval.x, self.oval.y)

    def ball_y_in_right_zone(self):
        if self.brick.y < self.oval.y < self.paddle.y + self.paddle_offset:
            return True
        else:
            return False

    def ball_y_in_wrong_zone(self):
        y_in_wrong_down_zone = self.window.height - (self.window.height - self.paddle_offset - self.paddle.height)\
                               <= self.oval.y <= self.window.height
        y_in_wrong_top_zone = 0 <= self.oval.y <= 215
        if y_in_wrong_top_zone or y_in_wrong_down_zone:
            return True
        else:
            return False

    def check_obj(self):
        x = self.oval.x
        y = self.oval.y
        r = BALL_RADIUS
        self.obj = self.window.get_object_at(x, y)
        if self.obj is None:
            self.obj = self.window.get_object_at(x+r*2, y+r*2)
            if self.obj is None:
                self.obj = self.window.get_object_at(x+r*2, y+r*2)
                if self.obj is None:
                    self.obj = self.window.get_object_at(x, y+r*2)
                    if self.obj is None:
                        return None
                    else:
                        return self.obj
                else:
                    return self.obj
            else:
                return self.obj
        else:
            return self.obj

    def reset_oval(self):
        if self.ball_y_in_right_zone():
            return self.oval_position()
        else:
            self.ball_y_in_right_zone()

        # if self.ball_y_in_wrong_zone():
        #     self.oval_position()

    # set oval velocity
    def set_oval_velocity(self):
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = self.__dx
        self.__dy = INITIAL_Y_SPEED

    # in order to let "breakout.py" get the argument __dx and __dy
    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    # a function to turn self.click into True for triggering the game
    def set_start(self, event):
        self.click = True
