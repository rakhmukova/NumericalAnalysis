import math

from common.functions import print_lab
from integration_formula.gauss import GaussFormula

if __name__ == '__main__':
    def f(x):
        return math.cos(x ** 2)

    def p(x): return 1

    print_lab(5.2, 'Вычисление интегралов при помощи КФ Гаусса')
    print(f'Вариант 8. \nf(x)=cos(x**2)')

    degrees = [3, 6, 7, 8]
    gauss = GaussFormula(f, degrees)
    gauss.integrate()
