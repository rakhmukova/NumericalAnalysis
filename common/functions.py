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