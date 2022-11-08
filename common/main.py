from tabulate import tabulate


def print_lab(num, name):
    print(f"\nЛабораторная работа №{num}: {name}")


def tabulate_results(array, headers):
    return tabulate(array, headers, tablefmt="github", colalign=("left",), numalign="left")