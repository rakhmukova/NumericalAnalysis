import math
from common.functions import print_lab, tabulate_results as tab, abs_error
import copy
from sympy import *


class Differ:

    def __init__(self, func, first_der, second_der):
        self.a = 0
        self.h = 0
        self.m = 0
        self.nodes = []
        self.func = func
        self.real_first_der = first_der
        self.real_second_der = second_der

    def set_nodes(self):
        node = self.a
        for i in range(0, self.m + 1):
            self.nodes.append([node, self.func(node)])
            node += self.h

    # f^k - P^k = O(h^2)

    # Точка в начале таблицы
    def der_of_start_point(self):
        return (-3 * self.nodes[0][1] + 4 * self.nodes[1][1] - self.nodes[2][1]) / (2 * self.h)

    # Центральная разностная производная
    def der_of_middle_point(self, i):
        return (self.nodes[i + 1][1] - self.nodes[i - 1][1]) / (2 * self.h)

    # Точка в конце таблицы
    def der_of_end_point(self):
        return (3 * self.nodes[self.m][1] - 4 * self.nodes[self.m - 1][1] + self.nodes[self.m - 2][1]) / (2 * self.h)

    def calc_first_der(self, i):
        if i == 0:
            return self.der_of_start_point()
        elif i == self.m:
            return self.der_of_end_point()
        else:
            return self.der_of_middle_point(i)

    # Метод неопределенных коэффициентов
    def calc_second_der(self, i):
        # не можем применить методы
        if i == 0 or i == self.m:
            return 0
        return (self.nodes[i + 1][1] - 2 * self.nodes[i][1] + self.nodes[i - 1][1]) / (self.h ** 2)

    def input_params(self):
        self.a = float(input("Введите начальный узел a (0): ") or '0')
        self.m = int(input("Введите количество узлов (11): ") or '11') - 1
        self.h = float(input("Введите отступ h (0.025): ") or '0.025')

    def calc_derivatives(self):
        self.nodes = []
        self.set_nodes()
        print()
        print(tab(self.nodes, ["x_j", "f(x_j)"]))
        print()

        result = copy.deepcopy(self.nodes)
        for i in range(0, self.m + 1):
            first_der = self.calc_first_der(i)
            result[i].append(first_der)
            real_first_der = self.real_first_der(self.nodes[i][0])
            abs_err = abs_error(real_first_der, first_der)
            result[i].append(abs_err)
            result[i].append(abs_err / real_first_der)

        for i in range(0, self.m + 1):
            second_der = self.calc_second_der(i)
            result[i].append(second_der)
            if i == 0 or i == self.m:
                result[i].append(0)
                result[i].append(0)
                continue

            real_second_der = self.real_second_der(self.nodes[i][0])
            abs_err = abs_error(real_second_der, second_der)
            result[i].append(abs_err)
            result[i].append(abs_err / real_second_der)

        print(tab(result, ["x_i", "f(x_i)", "f'(x_i)", "abs f'", "rel f'", """ f"(x_i) """,
                           """ abs f" """, """ rel f" """]))


if __name__ == '__main__':
    print_lab(3.2, "Нахождение производных таблично-заданной функции по формулам численного дифференцирования")
    print("Вариант 8. f(x)=exp(1.5 * 4 * x)\n")

    k = 1.5 * 4
    def func(x): return math.exp(k * x)
    def first_der(x): return k * func(x)
    def second_der(x): return k * first_der(x)
    differ = Differ(func, first_der, second_der)

    to_quit = 1
    while to_quit == 1:
        differ.input_params()
        differ.calc_derivatives()
        to_quit = int(input("\nВведите 0, чтобы выйти. Другую цифру, чтобы повторить: "))
        print()
