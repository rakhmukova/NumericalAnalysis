import copy
import math

from sympy import symbols, simplify, lambdify

from common.functions import print_lab, tabulate_results, abs_error, execution_loop, input_borders
from lab1.main import find_roots
from common.integrate import Integration


class GaussIntegration:
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
            print(f'\nN={degree}')
            print(polynomials[degree])
            polynom = lambdify(x, polynomials[degree])
            func_polynomials.append(polynom)
            if degree == 0:
                continue
            polynom_nodes = find_roots(polynom, -1, 1, 100, self.eps)
            polynomials_nodes.append(polynom_nodes)

        tabulate_results(polynomials_nodes, title="Узлы многочленов Лежандра")

        coefficients = self.calc_coefficients(func_polynomials, polynomials_nodes)
        tabulate_results(coefficients, title="Коэффициенты КФ Гаусса")
        return polynomials_nodes, coefficients

    def integrate_for_custom_borders(self, degree, polynomials_nodes, coefficients, f=None, a=-1, b=1):
        custom_nodes = copy.deepcopy(polynomials_nodes[degree - 1])
        custom_coefficients = copy.deepcopy(coefficients[degree - 1])
        sum_int = 0
        half = (b - a) / 2
        middle = (b + a) / 2
        if f is None:
            f = self.f
        for i in range(degree):
            custom_coefficients[i] *= half
            custom_nodes[i] = half * custom_nodes[i] + middle
            sum_int += custom_coefficients[i] * f(custom_nodes[i])
        if [a, b] != [-1, 1]:
            tabulate_results(zip(custom_nodes, custom_coefficients), headers=['узел', 'коэфф'],
                             title=f'Узлы и коэффициенты КФ Гаусса для N={degree}')
        return sum_int

    def integrate_custom(self, polynomials_nodes, coefficients):
        a, b = input_borders()
        for degree in self.degrees:

            approximate_value = self.integrate_for_custom_borders(degree, polynomials_nodes, coefficients, a=a, b=b)
            integration = Integration(a, b, self.f, lambda x: 1)
            precise_value = integration.precise()
            print(f'\nПриближенное значение интеграла: {approximate_value}')
            print(f"Точное значение интеграла: {precise_value}")

    def check_for_polynomials(self, polynomials_nodes, coefficients):
        eps = math.pow(10, -12)
        print(f'\nПроверим точность для многочленов (eps = {eps}):')
        for degree in self.degrees:
            def polynom(x): return 2 * x ** (2 * degree - 1)
            integration = Integration(-1, 1, polynom, lambda x: 1)
            precise_value = integration.precise()
            approximate_value = self.integrate_for_custom_borders(degree, polynomials_nodes, coefficients, polynom)
            print(f'\nПриближенное значение интеграла: {approximate_value}')
            print(f"Точное значение интеграла: {precise_value}")
            if abs_error(precise_value, approximate_value) < eps:
                print('Проверка пройдена')
            else:
                print('Проверка не пройдена')

    def integrate(self):
        polynomials_nodes, coefficients = self.find_common_nodes_and_coefficients()
        self.check_for_polynomials(polynomials_nodes, coefficients)
        execution_loop(self.integrate_custom, polynomials_nodes, coefficients)


if __name__ == '__main__':
    # a = 0
    # b = math.pi / 4

    def f(x):
        return math.cos(x ** 2)

    def p(x): return 1

    print_lab(5.2, "Вычисление интегралов при помощи КФ Гаусса")
    print(f"Вариант 8. \nf(x)=cos(x**2)")

    degrees = [3, 6, 7, 8]
    gauss = GaussIntegration(f, degrees)
    gauss.integrate()
