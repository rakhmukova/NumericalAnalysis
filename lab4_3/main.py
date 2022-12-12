from sympy import symbols, lambdify, exp

from common.main import print_lab, tabulate_results
from lab4_1.integrate import Integration

if __name__ == '__main__':
    print_lab(4.3, 'Приближённое вычисление интеграла по составным квадратурным формулам')
    print(f"Вариант 8.\n")

    x = symbols('x')
    exp_func = exp(x)
    zero_func = 0
    poly_0_func = 1
    poly_1_func = x
    poly_2_func = x**2
    poly_3_func = x**3
    functions = [exp_func, poly_0_func, poly_1_func, poly_2_func, poly_3_func]
    derivatives = [
        [exp_func, exp_func, exp_func, exp_func],
        [zero_func, zero_func, zero_func, zero_func],
        [poly_0_func, zero_func, zero_func, zero_func],
        [poly_1_func, poly_0_func, zero_func, zero_func],
        [poly_2_func, poly_1_func, zero_func, zero_func],
    ]
    print(tabulate_results(zip(range(0, len(functions)), functions), ['Номер', 'Функция']))
    num_of_function = int(input('\nВведите номер функции (0): ') or '0')

    f = lambdify(x, functions[num_of_function])
    ders = list(map(lambda der : lambdify(x, der), derivatives[num_of_function]))

    a = float(input("Введите левый предел интегрирования (0.0): ") or '0')
    b = float(input("Введите правый предел интегрирования (1.0): ") or '1')
    m = int(input("Введите число промежутков деления (10): ") or '10')

    def p(x): return 1

    integration = Integration(a, b, f, p, m, ders)
    print(f'\nШаг h: {(b - a) / m}')
    precise_value = integration.precise()
    print(f"\nТочное значение интеграла: {precise_value}\n")

    methods_and_names = [
        (integration.left_rectangles, "левых прямоугольников"),
        (integration.right_rectangles, "правых прямоугольников"),
        (integration.middle_rectangles, "средних прямоугольников"),
        (integration.trapezes, "трапеций"),
        (integration.simpsons_multiple, "Симпсона"),
    ]

    for methods_and_name in methods_and_names:
        method, name = methods_and_name
        approximate_value = method()
        theoretical_error = integration.theoretical_error(method)
        print(f"Составная КФ {name} : {approximate_value}")
        absolute_error = abs(precise_value - float(approximate_value))
        print(f"Абсолютная погрешность: {absolute_error}")
        print(f'Относительная погрешность: {absolute_error / abs(precise_value)}')
        print(f'Теоретическая погрешность: {theoretical_error}\n')
