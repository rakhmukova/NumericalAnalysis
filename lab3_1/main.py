import math

import numpy as np

from common.functions import print_lab, tabulate_results as tab, abs_error, execution_loop
from lab1.main import Solver
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
        print(f"\nВведите степень интерполяционного многочлена не более {m} (10): ")
        n = int(input() or '10')

        while n > self.m:
            print(f"Значение степени многочлена не должно превышать {m}, введите другое значение: ")
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

    def find_roots(self, equation):
        n = 100
        solver = Solver(equation, self.a, self.b, n, self.eps)
        solver.separate_roots()
        return solver.bisection()

    def interpolate_with_first_method(self):
        self.reverse_nodes_and_values()
        print("\nПоменяем местами колонки в таблице:")
        print(tab(self.value_table, ["f(x_j)", "x_j"]))

        self.take_closest_points()
        print("\nВозьмем ближайшие n + 1 точку к f(x):")
        print(tab(self.value_table, ["f(x_j)", "x_j"]))

        lagrange_polynom = self.build_polynom()
        point_value = lagrange_polynom(self.func_value)

        print("\nКоэффициенты интерполяционного многочлена:")
        print(tab(zip(range(self.n), lagrange_polynom.coef[::-1]), ["k", "coeff"]))

        print(f"\nЗначение многочлена (искомая точка): {point_value}")
        func_value = self.func(point_value)
        print(f"Исходное значение функции: {self.func_value}")
        print(f"Приближенное значение функции в точке: {func_value}")
        print(f"Невязка: {abs_error(func_value, self.func_value)}")

        self.reverse_nodes_and_values()

    def interpolate_with_second_method(self):
        self.take_closest_points()
        # print("Возьмем ближайшие n + 1 точку к x:")
        # print(tab(self.value_table, ["x_j", "f(x_j)"]))

        lagrange_polynom = self.build_polynom()
        def equation(x): return lagrange_polynom(x) - self.func_value
        print("\nКоэффициенты интерполяционного многочлена:")
        tab(zip(range(self.n), lagrange_polynom.coef[::-1]), ["k", "coeff"])

        roots = self.find_roots(equation)
        print(f"\nИсходное значение функции: {self.func_value}")
        print(f"\nКорни многочлена и значения:")
        func_values = [self.func(root) for root in roots]
        abs_diff = [abs_error(func_value, self.func_value) for func_value in func_values]
        tab(zip(roots, func_values, abs_diff), ["x", "f(x)", "|f(x) - F|"])

    def input_params(self):
        self.func_value = float(input("Введите F (0.28): ") or '0.28')
        self.eps = 10 ** int(input("ε = 10^p. Введите p (-6): ") or '-6')
        self.input_polynom_degree()

    def execute(self, can_use_first_method):
        self.value_table = []
        self.fill_value_table()
        print(tab(self.value_table, ["x_j", "f(x_j)"]))

        self.input_params()

        if can_use_first_method:
            print("\nПервый способ (поиск значения обратной функции):")
            self.interpolate_with_first_method()
            print("\n------------------------------------------------------------------")

        self.value_table = []
        self.fill_value_table()
        print("\nВторой способ (поиск корней уравнения P(x) - F = 0):")
        self.interpolate_with_second_method()


if __name__ == '__main__':
    print_lab(3.1, " Задача обратного интерполирования функции")
    print("Вариант 8. f(x)=2sin(x)-x/2")

    def func(x): return math.sin(x) * 2 - x / 2

    m = int(input("Введите количество узлов (16): ") or '16') - 1
    a = float(input("Введите левую границу отрезка (0): ") or '0')
    b = float(input("Введите правую границу (1): ") or '1')

    interpolation = ReverseInterpolation(func, a, b, m)
    execution_loop(interpolation.execute, True)
