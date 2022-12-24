import math

from common.functions import print_lab, execution_loop, input_borders, input_param
from lab2.interpolation import Interpolation


if __name__ == '__main__':
    print_lab(2, "Задача алгебраического интерполирования функции")
    print("Вариант 8. f(x)=2sin(x)-x/2  a = 0,2  b = 0,7  x = 0.35  n = 7  m = 15")

    m = input_param('количество узлов интерполирования', int, 15) - 1
    a, b = input_borders(0.2, 0.7)

    def func(x): return 2 * math.sin(x) - x / 2  # -3 ** 6 + 2 * x ** 3 + x ** 2

    inter = Interpolation(m, a, b, func)
    execution_loop(inter.execute)
