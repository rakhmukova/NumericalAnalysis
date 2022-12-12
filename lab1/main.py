import numpy as np
import scipy.misc as sc
import math

from common.main import print_lab, tabulate_results


class Solver:

    def __init__(self, func, a, b, n, epsilon):
        self.func = func
        self.a = a
        self.b = b
        self.N = n
        self.epsilon = epsilon
        self.intervals = []

    def third_criterion_met(self, x):
        if self.func(x) * sc.derivative(self.func, x, n=2) <= 0:
            return False
        return True

    def separate_roots(self):
        h = (self.b - self.a) / self.N
        x1 = self.a
        x2 = self.a + h
        y1 = self.func(x1)
        for i in range(self.N):
            y2 = self.func(x2)
            if y1 * y2 <= 0:
                self.intervals.append((x1, x2))
            x1 += h
            x2 += h
            y1 = self.func(x1)

        print(f"\nОтделение корней:\n")
        print(tabulate_results(zip(range(1, len(self.intervals) + 1), self.intervals),
                               ["Номер", "Интервал"]))

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
        if not self.third_criterion_met(xi0):
            return None

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

    def bisection(self):
        print("\nБисекция:\n")
        bisection_results = self.apply_method(self.specify_bisection)
        print(tabulate_results(bisection_results,
                               ["Корень", "Количество шагов", "Длина последнего отрезка",
                                "Абсолоютная величина невязки"]))
        roots = [bisection_results[i][1] for i in range(len(bisection_results))]
        return roots

    def execute(self):
        self.separate_roots()

        print("\nБисекция:\n")
        bisection_results = self.apply_method(self.specify_bisection)
        print(tabulate_results(bisection_results,
                               ["Корень", "Количество шагов", "Длина последнего отрезка",
                                "Абсолоютная величина невязки"]))

        print("\nМетод Ньютона:\n")
        newton_results = self.apply_method(self.specify_newton)
        print(tabulate_results(newton_results,
                               ["Корень", "Количество шагов",
                                "Абсолоютная величина невязки"]))

        print("\nМодифицированный метод Ньютона:\n")
        newton_modified_results = self.apply_method(self.specify_newton_modified)
        print(tabulate_results(newton_modified_results,
                               ["Корень", "Количество шагов",
                                "Абсолоютная величина невязки"]))

        print("\nМетод секущих:\n")
        secant_results = self.apply_method(self.specify_secant)
        print(tabulate_results(secant_results,
                               ["Корень", "Количество шагов",
                                "Абсолоютная величина невязки"]))


if __name__ == '__main__':
    a = -15
    b = 5
    epsilon = math.pow(10, -5)
    N = 1000
    def func(x): return 4 * math.cos(x) + 0.3 * x

    print_lab(1, "ЧИСЛЕННЫЕ МЕТОДЫ РЕШЕНИЯ НЕЛИНЕЙНЫХ УРАВНЕНИЙ")
    print(f"Вариант 8. f(x)= 4cos(x) + 0,3x  a = {a}  b = {b} epsilon = {epsilon}")

    solver = Solver(func, a, b, N, epsilon)
    solver.execute()