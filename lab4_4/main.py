from sympy import symbols, lambdify, exp

from common.functions import print_lab, tabulate_results, abs_error
from common.integrate import Integration


def calc(methods_and_names):
    approximate_values = []
    for methods_and_name in methods_and_names:
        method, name = methods_and_name
        approximate_value = method()
        approximate_values.append(approximate_value)

    return approximate_values


def specify(jh, jhl, l, d):
    deg = l**(d + 1)
    return (deg * jhl - jh) / (deg - 1)


def generate_methods(integration):
    return [
        (integration.left_rectangles, "левых прямоугольников"),
        (integration.right_rectangles, "правых прямоугольников"),
        (integration.middle_rectangles, "средних прямоугольников"),
        (integration.trapezes, "трапеций"),
        (integration.simpsons_multiple, "Симпсона"),
    ]


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

    a = float(input("Введите левый предел интегрирования (0.0): ") or '0')
    b = float(input("Введите правый предел интегрирования (1.0): ") or '1')
    m = int(input("Введите m (100): ") or '100')
    l = int(input("Введите l (100): ") or '100')

    def p(x): return 1

    integration = Integration(a, b, f, p, m, ders)
    methods_and_names = generate_methods(integration)
    print(f'\nШаг h: {(b - a) / m}')
    precise_value = integration.precise()
    print(f"\nТочное значение интеграла: {precise_value}\n")

    jh = calc(methods_and_names)

    integration = Integration(a, b, f, p, m * l, ders)
    methods_and_names = generate_methods(integration)
    jhl = calc(methods_and_names)

    names = [methods_and_name[1] for methods_and_name in methods_and_names]
    absolute_errors = [abs_error(precise_value, float(approximate_value)) for approximate_value in jhl]
    results = zip(names, jhl, absolute_errors)
    tabulate_results(results, ['Составная КФ', 'Значение', 'Абсолютная погрешность'], "Значения для разбиения m * l")

    precision = [0, 0, 1, 1, 3]
    j = [specify(jh[i], jhl[i], l, precision[i]) for i in range(len(precision))]

    absolute_errors = [abs_error(precise_value, float(approximate_value)) for approximate_value in j]
    relative_errors = [absolute_error / abs(precise_value) for absolute_error in absolute_errors]
    results = zip(names, j, absolute_errors, relative_errors)
    tabulate_results(results, ['Составная КФ', 'Значение', 'Абсолютная погрешность', 'Относительная погрешность'],
                     "Уточненные значения по принципу Рунге")


if __name__ == '__main__':
    print_lab(4.3, 'Приближённое вычисление интеграла по составным квадратурным формулам')
    print(f"Вариант 8.\n")

    to_quit = 1
    while to_quit != 0:
        execute()
        to_quit = int(input("\nВведите 0, чтобы закрыть программу, другую цифру, чтобы продолжить: "))
