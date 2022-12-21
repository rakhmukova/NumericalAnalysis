from sympy import symbols, lambdify, exp

from common.functions import print_lab, tabulate_results, abs_error, execution_loop, input_borders
from integration_formula.compound import Compound
from integration_formula.precise import Precise


def execute():
    x = symbols('x')
    exp_func = exp(x)
    zero_func = 0
    poly_0_func = 1
    poly_1_func = x
    poly_2_func = x ** 2
    poly_3_func = x ** 3
    functions = [exp_func, poly_0_func, poly_1_func, poly_2_func, poly_3_func]
    derivatives = [
        [exp_func, exp_func, exp_func, exp_func],
        [zero_func, zero_func, zero_func, zero_func],
        [poly_0_func, zero_func, zero_func, zero_func],
        [poly_1_func, poly_0_func, zero_func, zero_func],
        [poly_2_func, poly_1_func, zero_func, zero_func],
    ]
    tabulate_results(zip(range(0, len(functions)), functions), ['Номер', 'Функция'])
    num_of_function = int(input('\nВведите номер функции (0): ') or '0')

    f = lambdify(x, functions[num_of_function])
    ders = list(map(lambda der: lambdify(x, der), derivatives[num_of_function]))

    a, b = input_borders(0, 1)
    m = int(input("Введите число промежутков деления (100): ") or '100')

    def p(x): return 1

    precise = Precise(a, b, f, p)
    precise_value = precise.integrate()
    print(f"\nТочное значение интеграла: {precise_value}\n")

    compound = Compound(a, b, f, p, m, ders)

    methods_and_names = [
        (compound.left_rectangles, "левых прямоугольников"),
        (compound.right_rectangles, "правых прямоугольников"),
        (compound.middle_rectangles, "средних прямоугольников"),
        (compound.trapezes, "трапеций"),
        (compound.simpsons_multiple, "Симпсона"),
    ]

    for methods_and_name in methods_and_names:
        method, name = methods_and_name
        approximate_value = method()
        theoretical_error = compound.theoretical_error(method)
        print(f"Составная КФ {name} : {approximate_value}")
        absolute_error = abs_error(precise_value, float(approximate_value))
        print(f"Абсолютная погрешность: {absolute_error}")
        print(f'Относительная погрешность: {absolute_error / abs(precise_value)}')
        print(f'Теоретическая погрешность: {theoretical_error}\n')


if __name__ == '__main__':
    print_lab(4.3, 'Приближённое вычисление интеграла по составным квадратурным формулам')
    print(f"Вариант 8.\n")

    execution_loop(execute)
