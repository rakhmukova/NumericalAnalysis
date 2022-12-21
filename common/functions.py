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


def input_borders(def_a=None, def_b=None):
    a = float(input(f"Введите левую границу отрезка ({def_a}): ") or def_a)
    b = float(input(f"Введите правую границу отрезка ({def_b}): ") or def_b)
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
