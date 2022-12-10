import copy

from numpy.linalg import linalg

from common.main import tabulate_results as tab

import scipy.integrate as integrate


class Integration:

    def __init__(self, a, b, f, p):
        self.a = a
        self.b = b
        self.f = f
        self.p = p

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
        return self.interval() * (1/8 * self.phi(self.a) + 3/8 * self.phi(self.a + h) + 3/8 * self.phi(self.a + 2 * h) + 1 /8 * self.phi(self.b))

    def left_rectangles(self):
        pass

    def right_rectangles(self):
        pass

    def middle_rectangles(self):
        pass

    def trapezes(self):
        pass

    def simpsons_multiple(self):
        pass

    def precise(self):
        return integrate.quad(self.phi, self.a, self.b)[0]