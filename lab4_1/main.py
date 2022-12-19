import math

from common.functions import print_lab, abs_error
from common.integrate import Integration

if __name__ == '__main__':
    a = 0
    b = 1

    def f(x):
        return math.sin(x)

    def p(x): return 1 / math.sqrt(1 - x)

    x1 = 1 / 6
    x2 = 1 / 2
    x3 = 5 / 6
    nodes = [x1, x2, x3]

    print_lab(4.1, "Точное и приближённое вычисление интеграла по квадратурным формулам")
    print(f"Вариант 8. \nf(x)=sin(x) \np(x) = 1/sqrt(1 - x) \na={a}  b={b}")

    integration = Integration(a, b, f, p)

    precise_value = integration.precise()
    approximate_value = integration.approximate(nodes)

    print(f"\nПриближенное значение интеграла: {approximate_value}")
    print(f"Точное значение интеграла: {precise_value}")
    abs_err = abs_error(precise_value, float(approximate_value))
    print(f"Значение абсолютной погрешности: {abs_err}")
    print(f"Значение относительной погрешности: {abs(abs_err/precise_value)}")