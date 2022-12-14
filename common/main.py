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