import math

from tabulate import tabulate


def print_lab(num, name):
    print(f"\nЛабораторная работа №{num}: {name}")


def tabulate_results(array, headers=None, title=None):
    if not array:
        return
    if title:
        print(f'\n{title}:\n')
    if not headers:
        headers = ()
    print(tabulate(array, headers, tablefmt="github", colalign=("left",), numalign="left"))


def abs_error(precise, approximate):
    return abs(precise - approximate)


def rel_error(precise, approximate):
    return abs_error(precise, approximate) / abs(precise)


def execution_loop(execute, *args):
    to_quit = 1
    while to_quit != 0:
        execute(*args)
        to_quit = int(input("\nВведите 0, чтобы выйти, другую цифру для ввода новых параметров: "))


def input_param(name, type, def_value=None):
    return type(input(f"Введите {name} ({def_value}): ") or def_value)


def input_borders(def_a=None, def_b=None):
    a = input_param('левую границу отрезка', float, def_a)
    b = input_param('правую границу отрезка', float, def_b)
    return a, b


def show_error_info(precise, approximate, show_rel_error=True):
    print(f"\nПриближенное значение: {approximate}")
    print(f"Точное (исходное) значение: {precise}")
    abs_err = abs_error(precise, float(approximate))
    print(f"Значение абсолютной погрешности: {abs_err}")
    if show_rel_error:
        print(f"Значение относительной погрешности: {abs(abs_err / precise)}")


def divide_epochs():
    print('\n---------------------------------------------------------------------------------')


def check_precision(precise, approximate, eps=math.pow(10, -12)):
    if abs_error(precise, approximate) < eps:
        if abs_error(precise, approximate) < eps:
            print('Проверка пройдена')
        else:
            print('Проверка не пройдена')
