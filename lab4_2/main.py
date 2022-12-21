import math

from sympy import symbols, exp, lambdify

from common.functions import print_lab, tabulate_results, abs_error, execution_loop, input_borders
from integration_formula.precise import Precise
from integration_formula.simple import Simple


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

    a, b = input_borders()
    def p(x): return 1
    precise = Precise(a, b, f, p)
    precise_value = precise.integrate()
    print(f"\nТочное значение интеграла: {precise_value}\n")

    simple = Simple(a, b, f, p)

    methods_and_names = [
        (simple.left_rectangle, "левого прямоугольника"),
        (simple.right_rectangle, "правого прямоугольника"),
        (simple.middle_rectangle, "среднего прямоугольника"),
        (simple.trapeze, "трапеции"),
        (simple.simpsons, "Симпсона (или парабол)"),
        (simple.three_eights, "3/8"),
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
