import copy
import math

from common.functions import tabulate_results, abs_error, execution_loop, input_borders, show_error_info
from integration_formula.gauss_base import GaussBase
from integration_formula.precise import Precise


class GaussFormula(GaussBase):
    def __init__(self, f, degrees):
        super().__init__(f, degrees)

    def integrate_for_custom_borders(self, degree, polynomials_nodes, coefficients, f=None, a=-1, b=1):
        custom_nodes = copy.deepcopy(polynomials_nodes[degree - 1])
        custom_coefficients = copy.deepcopy(coefficients[degree - 1])
        assert len(custom_nodes) == len(custom_coefficients) == degree
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
            precise = Precise(a, b, self.f, lambda x: 1)
            precise_value = precise.integrate()
            show_error_info(precise_value, approximate_value, show_rel_error=False)

    def check_for_polynomials(self, polynomials_nodes, coefficients):
        eps = math.pow(10, -12)
        print(f'\nПроверим точность для многочленов (eps = {eps}):')
        for degree in self.degrees:
            def polynom(x): return 2 * x ** (2 * degree - 1)
            precise = Precise(-1, 1, polynom, lambda x: 1)
            precise_value = precise.integrate()
            approximate_value = self.integrate_for_custom_borders(degree, polynomials_nodes, coefficients, polynom)
            show_error_info(precise_value, approximate_value, show_rel_error=False)
            if abs_error(precise_value, approximate_value) < eps:
                print('Проверка пройдена')
            else:
                print('Проверка не пройдена')

    def integrate(self):
        polynomials_nodes, coefficients = self.find_common_nodes_and_coefficients()
        self.check_for_polynomials(polynomials_nodes, coefficients)
        execution_loop(self.integrate_custom, polynomials_nodes, coefficients)
