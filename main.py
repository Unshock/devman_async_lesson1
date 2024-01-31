import time
import curses
from animations import fire, animate_spaceship
from drawing_tools import create_stars

TIC_TIMEOUT = 0.1 * 1


def draw_border(canvas):
    canvas.border()
    canvas.refresh()


def draw(canvas):
    stars_count = 100
    max_y, max_x = canvas.getmaxyx()

    fire_shot_coroutine = fire(
        canvas, start_row=max_y / 2, start_column=max_x / 2, rows_speed=-0.9
    )

    spaceship_coroutine = animate_spaceship(
        canvas, max_y=max_y, max_x=max_x
    )

    coroutines = [fire_shot_coroutine, spaceship_coroutine]

    stars = create_stars(canvas, stars_count, max_y, max_x)

    coroutines += stars

    while True:

        for coroutine in coroutines.copy():

            try:
                coroutine.send(None)

            except StopIteration:
                coroutines.remove(fire_shot_coroutine)

        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw_border)
    curses.curs_set(False)
    curses.wrapper(draw)
