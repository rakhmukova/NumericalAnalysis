import math

from numpy.linalg import linalg
from sympy import symbols

from common.main import print_lab, tabulate_results
from lab1.main import Solver

import scipy.integrate as integrate

from lab4_1.integrate import Integration


class GaussianQuadratic:

    def __init__(self, a, b, f, p, N):
        self.a = a
        self.b = b
        self.f = f
        self.p = p
        self.N = N
        self.eps = math.pow(10, -12)

    def find_roots(self, equation):
        n = 100
        solver = Solver(equation, self.a, self.b, n, self.eps)
        solver.separate_roots()
        return solver.bisection()

    def find_moments(self):
        moments = []
        for i in range(self.N * 2):
            moment = integrate.quad(lambda x: self.p(x) * x ** i, self.a, self.b)[0]
            moments.append(moment)

        return moments

    def find_polynom_coefficients(self, moments):
        matrix = []
        for i in range(self.N):
            row = moments[i:self.N + i][::-1]
            matrix.append(row)
        right_part = moments[self.N:self.N * 2]
        print(f'\nМатрица линейной системы: ')
        print(tabulate_results(matrix, []))
        print(f'\nПравая часть линейной системы: ')
        print(tabulate_results(zip([f"m_{self.N - 1 + j}" for j in range(len(right_part))], right_part), []))
        coefficients = list(linalg.solve(matrix, right_part))
        return coefficients

    def build_polynom(self):
        moments = self.find_moments()
        print('Моменты весовой функции:\n')
        print(tabulate_results(zip(range(len(moments)), moments), ['i', 'm_i']))

        polynom_coefficients = self.find_polynom_coefficients(moments)
        print('\nКоэффициенты ортогонального многочлена (решение системы):\n')
        print(tabulate_results(zip(range(1, len(polynom_coefficients) + 1), polynom_coefficients), ['i', 'A_i']))

        def polynom(x):
            result = 0
            polynom_coefficients.reverse()
            x_degree = 1
            for coefficient in polynom_coefficients:
                result += coefficient * x_degree
                x_degree *= x

            result += x_degree
            return result

        x = symbols('x')
        print(f'\nОртогональный многочлен: {polynom(x)}')
        return polynom

    def integrate(self):
        print(f'\n1. Построение ортогонального многочлена')
        polynom = self.build_polynom()
        print(f'\n2. Нахождение корней ортогонального многочлена -- узлов КФ')
        nodes = self.find_roots(polynom)
        print(f'\nКорни многочлена:\n')
        print(tabulate_results(zip([f"x_{j}" for j in range(len(nodes))], nodes), []))

        print(f'\n2. Нахождение коэффициентов A_k и построение КФ')
        integration = Integration(self.a, self.b, self.f, self.p)
        return integration.approximate(nodes)


if __name__ == '__main__':
    print_lab(5.1, "Приближённое вычисление интегралов при помощи КФ НАСТ")
    print(f"Вариант 8. f(x)=sin(x) p(x)=exp(x)\n")

    a = 0  # float(input("Введите левый предел интегрирования (0.0): ") or '0')
    b = 1  # float(input("Введите правый предел интегрирования (1.0): ") or '1')
    N = 10  # int(input("Введите количество узлов (10): ") or '3')


    def validation_polynom(x): return x ** (2 * N - 1)


    def f(x):
        return math.sin(x)


    def p(x): return math.exp(x)


    integration = Integration(a, b, validation_polynom, p)
    precise_value = integration.precise()

    gaussian = GaussianQuadratic(a, b, validation_polynom, p, N)
    approximate_value = gaussian.integrate()

    print(f"\nПриближенное значение интеграла: {approximate_value}")
    print(f"Точное значение интеграла: {precise_value}")
    abs_mistake = abs(precise_value - float(approximate_value))
    print(f"Значение абсолютной погрешности: {abs_mistake}")
    print(f"Значение относительной погрешности: {abs(abs_mistake / precise_value)}")
