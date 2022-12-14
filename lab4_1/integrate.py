import copy

import scipy
from numpy.linalg import linalg

from common.main import tabulate_results as tab

import scipy.integrate as integrate


class Integration:

    def __init__(self, a, b, f, p, m=None, ders=None):
        self.a = a
        self.b = b
        self.f = f
        self.p = p
        self.m = m
        self.h = None
        if m:
            self.h = self.interval() / self.m
        self.func_maximums = []
        self.find_max(ders)

    def find_max(self, ders):
        if ders is None:
            return
        for i in range(4):
            func_max = scipy.optimize.minimize_scalar(lambda x: -ders[i](x), bounds=[self.a, self.b],
                                                      method='bounded')
            self.func_maximums.append(-func_max['fun'])

    def phi(self, x):
        return self.p(x) * self.f(x)

    def interval(self):
        return self.b - self.a

    def middle_point(self):
        return (self.b + self.a) / 2

    def approximate(self, nodes):
        n = len(nodes)
        moments = []
        matrix = []
        for i in range(n):
            row = list(map(lambda x: x ** i, copy.deepcopy(nodes)))
            matrix.append(row)

            moment = integrate.quad(lambda x: self.p(x) * x ** i, self.a, self.b)[0]
            moments.append(moment)

        print("\nМоменты:")
        print(tab(zip([f"m_{j}" for j in range(n)], moments), []))

        print("\nМатрица:")
        print(tab(matrix, [f"x_{i}" for i in range(len(nodes))]))

        coefficients = list(linalg.solve(matrix, moments))
        print("\nКоэффициенты (решение линейного уравнения):")
        print(tab(zip([f"A_{j}" for j in range(n)], coefficients), []))

        value = 0
        for i in range(n):
            value += coefficients[i] * self.f(nodes[i])
        return value

    # d = 0
    def left_rectangle(self):
        return self.interval() * self.phi(self.a)

    def right_rectangle(self):
        return self.interval() * self.phi(self.b)

    # d = 1
    def middle_rectangle(self):
        return self.interval() * self.phi(self.middle_point())

    def trapeze(self):
        return (self.interval() / 2) * (self.phi(self.a) + self.phi(self.b))

    # d = 3
    def simpsons(self):
        return (self.interval() / 6) * (self.phi(self.a) + 4 * self.phi(self.middle_point()) + self.phi(self.b))

    def three_eights(self):
        h = self.interval() / 3
        return self.interval() * (1 / 8 * self.phi(self.a) + 3 / 8 * self.phi(self.a + h) + 3 / 8 * self.phi(
            self.a + 2 * h) + 1 / 8 * self.phi(self.b))

    # 2 (f(A + h) + ... + f(B-h))
    def __double_part(self):
        result = 0
        x = self.a + self.h
        for i in range(self.m - 1):
            result += self.f(x)
            x += self.h
        return 2 * result

    def __sum_of_ends(self):
        return self.f(self.a) + self.f(self.b)

    def __middle_part(self):
        result = 0
        x = self.a + self.h / 2
        for i in range(self.m):
            result += self.f(x)
            x += self.h
        return result

    def left_rectangles(self):
        result = 0
        x = self.a
        for i in range(self.m):
            result += self.f(x)
            x += self.h
        return result * self.h

    def right_rectangles(self):
        result = 0
        x = self.a
        for i in range(self.m):
            x += self.h
            result += self.f(x)
        return result * self.h

    def middle_rectangles(self):
        return self.__middle_part() * self.h

    def trapezes(self):
        result = self.__double_part() + self.__sum_of_ends()
        return (result * self.h) / 2

    def simpsons_multiple(self):
        result = self.__sum_of_ends() + self.__double_part() + self.__middle_part() * 4
        return (result * self.h) / 6

    def precise(self):
        return integrate.quad(self.phi, self.a, self.b)[0]

    def theoretical_error(self, method):
        algebraic_precision_and_const_value = {
            self.left_rectangles: [0, 1 / 2],
            self.right_rectangles: [0, 1 / 2],
            self.middle_rectangles: [1, 1 / 24],
            self.trapezes: [1, 1 / 12],
            self.simpsons_multiple: [3, 1 / 2880]
        }

        d, value = algebraic_precision_and_const_value[method]
        func_max = self.func_maximums[d]
        # print(value)
        # print(func_max)
        # print(self.interval())
        # print(self.h ** (d + 1))
        result = value * func_max * self.interval() * self.h ** (d + 1)
        # print(result)
        return result
