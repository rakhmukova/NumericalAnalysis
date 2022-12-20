import math

from sympy import symbols, exp, lambdify

from common.functions import print_lab, tabulate_results, abs_error, execution_loop
from common.integrate import Integration


def execute():
    x = symbols('x')
    exp_func = exp(x)
    poly_0_func = 1
    poly_1_func = x
    poly_2_func = x ** 2
    poly_3_func = x ** 3
    functions = [exp_func, poly_0_func, poly_1_func, poly_2_func, poly_3_func]
    tabulate_results(zip(range(0, len(functions)), functions), ['Номер', 'Функция'])
    num_of_function = int(input('\nВведите номер функции (0): ') or '0')

    f = lambdify(x, functions[num_of_function])

    a = float(input("Введите левый предел интегрирования: "))
    b = float(input("Введите правый предел интегрирования: "))
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
        print(f"Абсолютная погрешность: {abs_error(precise_value, float(approximate_value))}\n")


if __name__ == '__main__':
    def f(x):
        return math.exp(x)

    print_lab(4.2, 'Приближённое вычисление интеграла по простым квадратурным формулам')
    print(f"Вариант 8")

    execution_loop(execute)
