import math

from common.functions import print_lab, input_borders, show_error_info
from integration_formula.approximate import Approximate
from integration_formula.precise import Precise

if __name__ == '__main__':
    print_lab(4.1, 'Точное и приближённое вычисление интеграла по квадратурным формулам')
    print(f'Вариант 8. \nf(x)=sin(x) \np(x) = 1/sqrt(1 - x)')

    a, b = input_borders(0, 1)

    def f(x):
        return math.sin(x)

    def p(x): return 1 / math.sqrt(1 - x)

    x1 = 1 / 6
    x2 = 1 / 2
    x3 = 5 / 6
    nodes = [x1, x2, x3]

    precise = Precise(a, b, f, p)
    precise_value = precise.integrate()

    approximate = Approximate(a, b, f, p)
    approximate_value = approximate.integrate(nodes)
    
    show_error_info(precise_value, approximate_value)
