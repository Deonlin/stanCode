from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 1000 / 120  # 120 frames per second.
NUM_LIVES = 3


def main():
    lives = NUM_LIVES
    graphics = BreakoutGraphics()
    __dx = graphics.get_dx()
    __dy = graphics.get_dy()

    # Add animation loop here!
    while lives != 0:
        if graphics.click:
            graphics.oval.move(__dx, __dy)
        if graphics.oval.x <= 0 or graphics.oval.x + graphics.oval.width >= graphics.window.width:
            __dx = -__dx
        elif graphics.oval.y <= 0 or graphics.oval.y + graphics.oval.height >= graphics.window.height:
            __dy = -__dy

        if graphics.check_obj() is graphics.paddle:
            __dy = -graphics.get_dy()
        elif graphics.check_obj() is not graphics.paddle and graphics.check_obj() is not None:
            __dy = -__dy
            graphics.window.remove(graphics.check_obj())
            graphics.num_brick -= 1
        elif graphics.window.height <= graphics.oval.y + graphics.oval.height:
            graphics.reset_oval()
            graphics.click = False
            lives -= 1
        elif graphics.num_brick == 0:
            break

        if lives == 0:
            break
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
