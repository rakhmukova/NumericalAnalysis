import math

from sympy import symbols

from common.functions import tabulate_results, show_error_info, divide_epochs
from integration_formula.approximate import Approximate
from integration_formula.precise import Precise
from lab1.main import find_roots
from numpy.linalg import linalg

import scipy.integrate as integrate


class GaussianFormula:

    def __init__(self, a, b, f, p, N):
        self.a = a
        self.b = b
        self.f = f
        self.p = p
        self.N = N
        self.eps = math.pow(10, -12)

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
        right_part = list(map(lambda m: -m, moments[self.N:self.N * 2]))
        tabulate_results(matrix, title="Матрица линейной системы")
        tabulate_results(zip([f"m_{self.N - 1 + j}" for j in range(len(right_part))], right_part),
                         title="Правая часть линейной системы")
        coefficients = list(linalg.solve(matrix, right_part))
        return coefficients

    def build_polynom(self):
        moments = self.find_moments()
        tabulate_results(zip(range(len(moments)), moments), ['i', 'm_i'], "Моменты весовой функции")

        polynom_coefficients = self.find_polynom_coefficients(moments)
        tabulate_results(zip(range(1, len(polynom_coefficients) + 1), polynom_coefficients), ['i', 'A_i'],
                         "Коэффициенты ортогонального многочлена (решение системы)")

        polynom_coefficients.reverse()

        def polynom(x):
            result = 0
            x_degree = 1
            for coefficient in polynom_coefficients:
                result += coefficient * x_degree
                x_degree *= x

            result += x_degree
            return result

        x = symbols('x')
        print(f'\nОртогональный многочлен: {polynom(x)}')
        return polynom

    def highest_degree(self):
        return self.N * 2 - 1

    def check_for_polynom(self, nodes):
        def polynom(x):
            return x ** self.highest_degree()

        precise = Precise(self.a, self.b, polynom, self.p)
        precise_value = precise.integrate()

        approximate = Approximate(self.a, self.b, polynom, self.p)
        approximate_value = approximate.integrate(nodes)

        show_error_info(precise_value, approximate_value)

    def integrate(self):
        divide_epochs()
        print(f'\n1. Построение ортогонального многочлена')
        polynom = self.build_polynom()

        divide_epochs()
        print(f'\n2. Нахождение корней ортогонального многочлена -- узлов КФ')
        nodes = find_roots(polynom, self.a, self.b, 100, self.eps)
        tabulate_results(zip([f"x_{j}" for j in range(len(nodes))], nodes), title="Корни многочлена")

        divide_epochs()
        print(f'\n3. Проверка точности на полиноме степени {self.highest_degree()}')
        self.check_for_polynom(nodes)

        divide_epochs()
        print(f'\n4. Нахождение коэффициентов A_k и построение КФ')
        approximate = Approximate(self.a, self.b, self.f, self.p)
        return approximate.integrate(nodes)