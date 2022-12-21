import math

from common.functions import print_lab, execution_loop
from integration_formula.compound_gauss import CompoundGaussFormula

if __name__ == '__main__':

    def f(x):
        return math.sin(x)


    def p(x): return math.exp(x)

    print_lab(5.3, "Приближённое вычисление интеграла при помощи составной КФ Гаусса")
    print(f"Вариант 8. \nf(x)=sin(x) \np(x)=exp(x)")

    def execute():
        N = 10 # int(input('\nВведите N: '))
        degrees = [N]
        gauss = CompoundGaussFormula(f, degrees)
        gauss.integrate_compound()

    execution_loop(execute)
