import math

from sympy import symbols, simplify, lambdify

from common.functions import tabulate_results
from lab1.main import find_roots


class GaussBase:
    def __init__(self, f, degrees):
        self.f = f
        self.degrees = degrees
        self.N = max(degrees)
        self.eps = math.pow(10, -12)

    def build_polynomials(self):
        x = symbols('x')
        p0 = 1
        p1 = x
        polynomials = [p0, p1]

        for i in range(2, self.N + 1):
            p2 = x * ((2 * i - 1) / i) * p1 - (i - 1) / i * p0
            polynomials.append(p2)
            p0, p1 = p1, p2

        return list(map(lambda p: simplify(p), polynomials))

    def calc_coefficients(self, polynomials, nodes):
        coefficients = []
        for i in range(self.N):
            node = nodes[i]
            polynom = polynomials[i]
            current_coefficients = [2*(1 - node[j]**2) / (((i + 1) * polynom(node[j]))**2) for j in range(i + 1)]
            coefficients.append(current_coefficients)

        return coefficients

    def find_common_nodes_and_coefficients(self):
        polynomials = self.build_polynomials()
        tabulate_results(zip(range(len(polynomials)), polynomials), ['i', 'P_i'], "Многочлены Лежандра")

        polynomials_nodes = []
        func_polynomials = []
        x = symbols('x')
        for degree in range(self.N + 1):
            # print(f'\nN={degree}')
            # print(polynomials[degree])
            polynom = lambdify(x, polynomials[degree])
            func_polynomials.append(polynom)
            if degree == 0:
                continue
            polynom_nodes = find_roots(polynom, -1, 1, 100, self.eps)
            polynomials_nodes.append(polynom_nodes)

        coefficients = self.calc_coefficients(func_polynomials, polynomials_nodes)

        for degree in range(self.N):
            tabulate_results(zip(polynomials_nodes[degree], coefficients[degree]), headers=['t_k', 'A_k'],
                             title=f"Узлы и коэффициенты для N={degree + 1}")
            # tabulate_results(coefficients[degree], title="Коэффициенты КФ Гаусса")

        return polynomials_nodes, coefficients
