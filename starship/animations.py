import asyncio
import curses
import itertools
from common_tools import read_from_file
from curses_tools import read_controls, get_frame_size, draw_frame


async def fire(canvas, start_row, start_column, rows_speed=-0.3,
               columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 1 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def blink(canvas, row, column, symbol='*', start_pause=0):
    for tic in range(start_pause):
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

    while True:

        for tic in range(20):
            canvas.addstr(row, column, symbol, curses.A_DIM)
            await asyncio.sleep(0)

        for tic in range(3):
            canvas.addstr(row, column, symbol)
            await asyncio.sleep(0)

        for tic in range(5):
            canvas.addstr(row, column, symbol, curses.A_BOLD)
            await asyncio.sleep(0)

        for tic in range(3):
            canvas.addstr(row, column, symbol)
            await asyncio.sleep(0)


async def animate_spaceship(canvas, max_y, max_x, tics=2):
    rocket_frame_1 = read_from_file('starship/frames/rocket_frame_1.txt')
    rocket_frame_2 = read_from_file('starship/frames/rocket_frame_2.txt')

    row = max_y // 2 - 2
    column = max_x // 2 - 2

    for frame in itertools.cycle((rocket_frame_1, rocket_frame_2)):

        frame_height, frame_width = get_frame_size(frame)

        for tic in range(tics):

            canvas.nodelay(True)
            rows_change, columns_change, _ = read_controls(canvas)

            if rows_change or columns_change:
                row = max(
                    min(max_y - frame_height - 1,
                        row + rows_change),
                    1
                )

                column = max(
                    min(max_x - frame_width - 1,
                        column + columns_change),
                    1
                )

            draw_frame(canvas, row, column, frame)
            canvas.refresh()
            draw_frame(canvas, row, column, frame, negative=True)
            await asyncio.sleep(0)
