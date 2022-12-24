import math

from common.functions import print_lab, execution_loop
from lab3_2.differentiation import Differentiation

if __name__ == '__main__':
    print_lab(3.2, 'Нахождение производных таблично-заданной функции по формулам численного дифференцирования')
    print('Вариант 8. f(x)=exp(1.5 * 4 * x)\n')

    k = 1.5 * 4


    def func(x): return math.exp(k * x)


    def first_der(x): return k * func(x)


    def second_der(x): return k * first_der(x)


    differentiation = Differentiation(func, first_der, second_der)


    def execute():
        differentiation.input_params()
        differentiation.calc_derivatives()


    execution_loop(execute)
