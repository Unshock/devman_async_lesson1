from random import choice, randint
from starship.animations import blink


def get_random_star_coords(max_y, max_x):
    return randint(1, max_y - 2), randint(1, max_x - 2)


def get_random_star_icon():
    icons = ['+', '*', '.', ':']
    return choice(icons)


def create_stars(canvas, stars_count, max_y, max_x) -> list:
    stars_list = []

    for _ in range(stars_count):
        row, col = get_random_star_coords(max_y, max_x)
        icon = get_random_star_icon()
        start_pause = randint(1, 50)
        star_coroutine = blink(
            canvas, row, col, symbol=icon, start_pause=start_pause
        )

        stars_list.append(star_coroutine)

    return stars_list
