import copy

from integration_formula.integration import Integration

import scipy.integrate as integrate

from numpy.linalg import linalg

from common.functions import tabulate_results as tab


class Approximate(Integration):
    def __init__(self, a, b, f, p):
        super().__init__(a, b, f, p)

    def integrate(self, nodes):
        n = len(nodes)
        moments = []
        matrix = []
        for i in range(n):
            row = list(map(lambda x: x ** i, copy.deepcopy(nodes)))
            matrix.append(row)

            moment = integrate.quad(lambda x: self.p(x) * x ** i, self.a, self.b)[0]
            moments.append(moment)

        tab(zip([f"m_{j}" for j in range(n)], moments), title="Моменты")

        tab(matrix, [f"x_{i}" for i in range(len(nodes))], "Матрица")

        coefficients = list(linalg.solve(matrix, moments))
        tab(zip([f"A_{j}" for j in range(n)], coefficients), title="Коэффициенты (решение линейного уравнения)")

        value = 0
        for i in range(n):
            value += coefficients[i] * self.f(nodes[i])
        return value