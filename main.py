from random import randint
from copy import deepcopy
from mouse import get_position
from painter import Painter


def get_base_pole() -> list[list[int], ]:
    return [[0] * (count_bots + 2) for _ in range(count_bots + 2)]


def get_random_pole() -> list[list[int], ]:
    for i in range(1, len(pole) - 1):
        for j in range(1, len(pole) - 1):
            if randint(0, count_bots // rate_bots) == 1:
                pole[i][j] = 1
            else:
                pole[i][j] = 0

    return pole


def sum_el(i, j, const_pole):
    count = sum(const_pole[i - 1][j - 1:j + 2])
    count += const_pole[i][j - 1] + const_pole[i][j + 1]
    count += sum(const_pole[i + 1][j - 1:j + 2])

    return count


def run_main_loop() -> None:
    const_pole = deepcopy(pole)

    for i in range(1, len(pole) - 1):
        for j in range(1, len(pole) - 1):
            count = sum_el(i, j, const_pole)

            if not pole[i][j] and count == 3:
                pole[i][j] = 1
            elif pole[i][j] and (count == 2 or count == 3):
                pass
            else:
                pole[i][j] = 0

            add_rules(i, j)

    painter.render_pole(pole)

    painter.starter_fun_in_loop(run_main_loop)


def add_rules(i: int, j: int) -> None:
    # rule_1(i, j)
    # rule_1(j, i)
    # rule_2(i, j)
    rule_3(i, j)
    pass


def rule_1(i, j):
    if i % 10 == 0:
        pole[i][j] = 0


def rule_2(i, j):
    if i == j:
        pole[i][j] = 0


def rule_3(i, j):
    if i == 1 or i == len(pole) - 2 or j == 1 or j == len(pole) - 2:
        pole[i][j] = 0


def painted_bot_on_click() -> None:
    x, y = get_position()
    win_x, win_y = painter.get_par_win()

    x -= win_x
    y -= win_y

    if 0 <= x < painter.size_pole and 0 <= y < painter.size_pole:
        x //= painter.size_bots
        y //= painter.size_bots

        x += 1
        y += 1

        pole[y][x] = int(not pole[y][x])

        painter.render_pole(pole)


def set_base_pole():
    global pole
    pole = get_random_pole()
    painter.render_pole(pole)


def remove_pole():
    global pole
    pole = get_base_pole()
    get_random_pole()

    if painter.id_run_fun:
        painter.cancel_after()

    painter.render_pole(pole)


def initiate_events():
    painter.tk.bind('<BackSpace>', lambda e: remove_pole())
    painter.tk.bind('<1>', lambda e: painted_bot_on_click())
    painter.tk.bind('<Return>', lambda e: painter.starter_fun_in_loop(run_main_loop))
    painter.tk.bind('<plus>', lambda e: painter.increase_time_loop())
    painter.tk.bind('<minus>', lambda e: painter.reduce_time_loop())


def main():
    initiate_events()
    painter.run_painter_loop()


if __name__ == '__main__':
    # count_bots = 10

    size_pole = int(input('Введите размер поля в пикселях - '))
    count_bots = int(input('Введите максимальное количество ботов в строке (столбце) - '))
    rate_bots = int(input('Введите частоту попоявления ботов в строке (столбце) - '))

    painter = Painter(size_pole=size_pole, count_bots=count_bots, time_loop=1_000)

    pole = get_base_pole()
    get_random_pole()

    main()
