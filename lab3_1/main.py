import math

from common.functions import print_lab, execution_loop, input_borders, input_param

from lab3_1.reverse_interpolation import ReverseInterpolation

if __name__ == '__main__':
    print_lab(3.1, ' Задача обратного интерполирования функции')
    print('Вариант 8. f(x)=2sin(x)-x/2')

    def func(x): return math.sin(x) * 2 - x / 2

    m = input_param('количество узлов', int, 16) - 1
    a, b = input_borders(0, 1)

    interpolation = ReverseInterpolation(func, a, b, m)
    execution_loop(interpolation.execute, True)
