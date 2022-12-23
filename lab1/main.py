import copy

import numpy as np
import scipy.misc as sc
import math

from common.functions import print_lab, tabulate_results, execution_loop, input_borders, input_param


class Solver:

    def __init__(self, func, a, b, n, epsilon):
        self.func = func
        self.a = a
        self.b = b
        self.N = n
        self.epsilon = epsilon
        self.intervals = []

        self.methods_info = {
            self.separate_roots: {
                'name': 'Отделение корней',
                'results': ["Номер", "Интервал"]
            },
            self.specify_bisection: {
                'name': 'Метод бисекции',
                'results': ["Корень", "Количество шагов", "Длина последнего отрезка",
                            "Абсолоютная величина невязки"]
            },
            self.specify_newton: {
                'name': 'Метод Ньютона',
                'results': ["Корень", "Количество шагов",
                            "Абсолоютная величина невязки"]
            },
            self.specify_newton_modified: {
                'name': 'Модифицированный метод Ньютона',
                'results': ["Корень", "Количество шагов",
                            "Абсолоютная величина невязки"]
            },
            self.specify_secant: {
                'name': 'Метод секущих',
                'results': ["Корень", "Количество шагов",
                            "Абсолоютная величина невязки"]
            }
        }

    def third_criterion_met(self, x):
        if self.func(x) * sc.derivative(self.func, x, n=2) <= 0:
            return False
        return True

    def separate_roots(self):
        h = (self.b - self.a) / self.N
        print(f'Шаг h={h}\n')
        x1 = self.a
        x2 = self.a + h
        y1 = self.func(x1)
        for i in range(self.N):
            y2 = self.func(x2)
            if y1 * y2 <= 0:
                self.intervals.append((x1, x2))
            x1 += h
            x2 += h
            y1 = y2

        # print(self.intervals)
        return zip(range(1, len(self.intervals) + 1), copy.deepcopy(self.intervals))

    def specify_bisection(self, ai, bi):
        step = 0
        while (bi - ai) > 2 * self.epsilon:
            c = (ai + bi) / 2
            if self.func(ai) * self.func(c) <= 0:
                bi = c
            else:
                ai = c
            step += 1
        x = (ai + bi) / 2
        return [x, step, bi - ai, abs(self.func(x) - 0)]

    def specify_newton(self, ai, bi):
        xi = (ai + bi) / 2
        xi1 = xi - self.func(xi) / sc.derivative(self.func, xi)
        if not self.third_criterion_met(xi):
            return None

        step = 0
        while np.abs(xi1 - xi) >= self.epsilon:
            xi = xi1
            xi1 = xi - self.func(xi) / sc.derivative(self.func, xi)
            step += 1

        return [xi1, step, abs(self.func(xi1) - 0)]

    def specify_newton_modified(self, ai, bi):
        xi = (ai + bi) / 2
        f_der_x0 = sc.derivative(self.func, xi)
        xi1 = xi - self.func(xi) / f_der_x0
        if not self.third_criterion_met(xi):
            return None

        step = 0
        while np.abs(xi1 - xi) >= self.epsilon:
            xi = xi1
            xi1 = xi - self.func(xi) / f_der_x0
            step += 1

        return [xi1, step, abs(self.func(xi1) - 0)]

    def specify_secant(self, ai, bi):
        xi0 = (ai + bi) / 2
        xi1 = ai
        xi2 = bi
        # if not self.third_criterion_met(xi0):
        #     return None

        step = 0
        while abs(xi1 - xi2) > self.epsilon:
            xi0, xi1, xi2 = xi1, xi2, xi1 - (self.func(xi1) / (self.func(xi1) - self.func(xi0))) * (xi1 - xi0)
            step += 1

        return [xi2, step, abs(self.func(xi2) - 0)]

    def apply_method(self, method):
        results = []
        for i in range(0, len(self.intervals)):
            result = method(self.intervals[i][0], self.intervals[i][1])
            if result is None:
                continue
            results.append([i + 1] + result)

        if len(results) != len(self.intervals):
            print("Другие корни нельзя уточнить. Третье условие теоремы о сходимости не выполнено\n")
        return results

    def call_method(self, method, print_info=True):
        method_info = self.methods_info[method]
        if print_info:
            print(f'''\n{method_info['name']}\n''')
        results = None
        if method == self.separate_roots:
            results = method()
        else:
            results = self.apply_method(method)
        if print_info:
            tabulate_results(results, method_info['results'])
        return results

    def execute(self):
        methods = [
            self.separate_roots,
            self.specify_bisection,
            self.specify_newton,
            self.specify_newton_modified,
            self.specify_secant
        ]

        for method in methods:
            self.call_method(method)


def find_roots(equation, a, b, N, epsilon, method_name='bisection', print_info=True):
    solver = Solver(equation, a, b, N, epsilon)
    solver.call_method(solver.separate_roots, print_info)

    methods = {
        'bisection': solver.specify_bisection,
        'newton': solver.specify_newton,
        'newton_modified': solver.specify_newton_modified,
        'secant': solver.specify_secant
    }

    method_result = solver.call_method(methods[method_name], print_info)
    return [method_result[i][1] for i in range(len(method_result))]


if __name__ == '__main__':
    epsilon = math.pow(10, -5)


    def func(x): return 4 * math.cos(x) + 0.3 * x


    print_lab(1, "ЧИСЛЕННЫЕ МЕТОДЫ РЕШЕНИЯ НЕЛИНЕЙНЫХ УРАВНЕНИЙ")
    print(f"Вариант 8. f(x)= 4cos(x) + 0,3x epsilon = {epsilon}")


    def execute():
        a, b = input_borders(-15, 5)
        N = input_param('N', int, 1000)
        pow = input_param('степень точности', int, -5)
        epsilon = math.pow(10, pow)
        solver = Solver(func, a, b, N, epsilon)
        solver.execute()


    execution_loop(execute)
