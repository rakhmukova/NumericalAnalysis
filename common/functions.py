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


def abs_error(real, pred):
    return abs(real - pred)


def rel_error(real, pred):
    return abs_error(real, pred) / abs(real)


def execution_loop(execute, *args):
    to_quit = 1
    while to_quit != 0:
        execute(*args)
        to_quit = int(input("\nВведите 0, чтобы закрыть программу, другую цифру, чтобы продолжить: "))


def input_borders(def_a=None, def_b=None):
    a = float(input(f"Введите левую границу отрезка ({def_a}): ") or def_a)
    b = float(input(f"Введите правую границу ({def_b}): ") or def_b)
    return a, b
