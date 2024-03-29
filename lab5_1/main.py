import math

from common.functions import print_lab, input_borders, show_error_info, execution_loop, input_param
from integration_formula.gaussian import GaussianFormula
from integration_formula.precise import Precise


def execute():
    a, b = input_borders(0, 1)
    N = input_param('количество узлов', int, 10)

    def f(x):
        return math.sin(x)

    def p(x): return math.exp(x)

    precise = Precise(a, b, f, p)
    precise_value = precise.integrate()

    gaussian = GaussianFormula(a, b, f, p, N)
    approximate_value = gaussian.integrate()

    show_error_info(precise_value, approximate_value)


if __name__ == '__main__':
    print_lab(5.1, 'Приближённое вычисление интегралов при помощи КФ НАСТ')
    print(f'Вариант 8. \nf(x)=sin(x) \np(x)=exp(x)\n')

    execution_loop(execute)
