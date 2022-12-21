from common.functions import execution_loop, input_borders, show_error_info
from integration_formula.gauss_base import GaussBase
from integration_formula.precise import Precise


class CompoundGaussFormula(GaussBase):
    def __init__(self, f, degrees):
        super().__init__(f, degrees)

    def integrate_compound_for_borders(self, degree, polynomials_nodes, coefficients, a=-1, b=1, m=1, func=None):
        h = (b - a) / m
        custom_nodes = polynomials_nodes[degree - 1]
        custom_coefficients = coefficients[degree - 1]
        assert len(custom_nodes) == len(custom_coefficients) == degree
        value = 0
        half = h / 2
        diffs = [a + h*j + half for j in range(m)]
        if func is None:
            func = self.f
        for k in range(len(custom_nodes)):
            nodes = [half * custom_nodes[k] + diffs[j] for j in range(m)]
            func_values = [func(node) for node in nodes]
            value += sum(func_values) * custom_coefficients[k] * half

        return value

    def integrate_custom_compound(self, polynomials_nodes, coefficients):
        a, b = input_borders(0, 10)
        m = 5  # int(input('Введите m: '))
        for degree in self.degrees:
            approximate_value = self.integrate_compound_for_borders(degree, polynomials_nodes, coefficients, a, b, m)
            precise = Precise(a, b, self.f, lambda x: 1)
            precise_value = precise.integrate()
            show_error_info(precise_value, approximate_value, show_rel_error=False)

    def integrate_compound(self):
        polynomials_nodes, coefficients = self.find_common_nodes_and_coefficients()
        # self.check_for_polynomials(polynomials_nodes, coefficients)
        execution_loop(self.integrate_custom_compound, polynomials_nodes, coefficients)