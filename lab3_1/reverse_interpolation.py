import numpy as np

from common.functions import tabulate_results, abs_error, show_error_info, divide_epochs
from lab1.equation_solver import find_roots
from scipy.interpolate import lagrange


class ReverseInterpolation:

    def __init__(self, func, a, b, m):
        self.func = func
        self.a = a
        self.b = b
        self.m = m

        self.func_value = None
        self.n = None
        self.eps = None

        self.value_table = []

    def fill_value_table(self):
        x_j = self.a
        h = (self.b - self.a) / self.m
        for j in range(self.m + 1):
            self.value_table.append([x_j, self.func(x_j)])
            x_j += h

    def input_polynom_degree(self):
        print(f'\nВведите степень интерполяционного многочлена не более {self.m} (10): ')
        n = int(input() or '10')

        while n > self.m:
            print(f'Значение степени многочлена не должно превышать {self.m}, введите другое значение: ')
            n = int(input())

        self.n = n

    def take_closest_points(self):
        # sort by distance from x and take first n + 1
        self.value_table = sorted(self.value_table, key=lambda t: abs(t[0] - self.func_value))
        self.value_table = self.value_table[:self.n + 1]
        # self.value_table = sorted(self.value_table, key=lambda t: t[0])

    def reverse_nodes_and_values(self):
        for pair in self.value_table:
            pair[0], pair[1] = pair[1], pair[0]

    def build_polynom(self):
        x = np.array([self.value_table[i][0] for i in range(self.n)])
        y = np.array([self.value_table[i][1] for i in range(self.n)])
        return lagrange(x, y)

    def interpolate_with_first_method(self):
        self.reverse_nodes_and_values()
        tabulate_results(self.value_table, ['f(x_j)', 'x_j'], title='Поменяем местами колонки в таблице')

        self.take_closest_points()
        tabulate_results(self.value_table, ['f(x_j)', 'x_j'], title='Возьмем ближайшие n + 1 точку к f(x)')

        lagrange_polynom = self.build_polynom()
        point_value = lagrange_polynom(self.func_value)

        tabulate_results(lagrange_polynom.coef[::-1], ['k', 'coeff'],
                         title='Коэффициенты интерполяционного многочлена')

        print(f'\nЗначение многочлена (искомая точка): {point_value}')
        func_value = self.func(point_value)
        show_error_info(self.func_value, func_value)

        self.reverse_nodes_and_values()

    def interpolate_with_second_method(self):
        self.take_closest_points()
        # tabulate_results(self.value_table, ['x_j', 'f(x_j)'], title='Возьмем ближайшие n + 1 точку к x)

        lagrange_polynom = self.build_polynom()

        def equation(x): return lagrange_polynom(x) - self.func_value

        tabulate_results(lagrange_polynom.coef[::-1], ['k', 'coeff'],
                         title='Коэффициенты интерполяционного многочлена')

        roots = find_roots(equation, self.a, self.b, 100, self.eps)
        print(f'\nИсходное значение функции: {self.func_value}')
        func_values = [self.func(root) for root in roots]
        abs_diff = [abs_error(func_value, self.func_value) for func_value in func_values]
        tabulate_results(zip(roots, func_values, abs_diff), ['x', 'f(x)', '|f(x) - F|'],
                         title='Корни многочлена и значения')

    def input_params(self):
        self.func_value = float(input('Введите F (0.28): ') or '0.28')
        self.eps = 10 ** int(input('ε = 10^p. Введите p (-6): ') or '-6')
        self.input_polynom_degree()

    def execute(self, can_use_first_method):
        self.value_table = []
        self.fill_value_table()
        tabulate_results(self.value_table, ['x_j', 'f(x_j)'])

        self.input_params()

        if can_use_first_method:
            print('\nПервый способ (поиск значения обратной функции):')
            self.interpolate_with_first_method()
            divide_epochs()

        self.value_table = []
        self.fill_value_table()
        print('\nВторой способ (поиск корней уравнения P(x) - F = 0):')
        self.interpolate_with_second_method()
