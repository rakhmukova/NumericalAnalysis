import math

from sympy import symbols, exp, lambdify

from common.main import print_lab, tabulate_results
from lab4_1.integrate import Integration


def execute():
    x = symbols('x')
    exp_func = exp(x)
    zero_func = 0
    poly_0_func = 1
    poly_1_func = x
    poly_2_func = x ** 2
    poly_3_func = x ** 3
    functions = [exp_func, poly_0_func, poly_1_func, poly_2_func, poly_3_func]
    print(tabulate_results(zip(range(0, len(functions)), functions), ['Номер', 'Функция']))
    num_of_function = int(input('\nВведите номер функции (0): ') or '0')

    f = lambdify(x, functions[num_of_function])

    a = int(input("Введите левый предел интегрирования: "))
    b = int(input("Введите правый предел интегрирования: "))
    def p(x): return 1
    integration = Integration(a, b, f, p)
    precise_value = integration.precise()
    print(f"\nТочное значение интеграла: {precise_value}\n")

    methods_and_names = [
        (integration.left_rectangle, "левого прямоугольника"),
        (integration.right_rectangle, "правого прямоугольника"),
        (integration.middle_rectangle, "среднего прямоугольника"),
        (integration.trapeze, "трапеции"),
        (integration.simpsons, "Симпсона (или парабол)"),
        (integration.three_eights, "3/8"),
    ]

    for methods_and_name in methods_and_names:
        method, name = methods_and_name
        approximate_value = method()
        print(f"КФ {name} : {approximate_value}")
        print(f"Абсолютная погрешность: {abs(precise_value - float(approximate_value))}\n")


if __name__ == '__main__':
    def f(x):
        return math.exp(x)

    print_lab(4.2, 'Приближённое вычисление интеграла по квадратурным формулам')
    print(f"Вариант 8")

    to_quit = 1
    while to_quit != 0:
        execute()
        to_quit = int(input("\nВведите 0, чтобы закрыть программу, другую цифру, чтобы продолжить: "))
