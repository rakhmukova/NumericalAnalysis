from common.functions import tabulate_results, abs_error


class Interpolation:

    @staticmethod
    def input_polynom_degree(m):
        print(f'\nВведите степень интерполяционного многочлена не более {m}: ')
        n = int(input())

        while n > m:
            print(f'Значение степени многочлена не должно превышать {m}, введите другое значение: ')
            n = int(input())

        return n

    def __init__(self, num_of_points, a, b, func):
        self.x = None
        self.a = a
        self.b = b
        self.func = func
        self.num_of_points = num_of_points
        self.value_table = []
        self.diff_table = []
        self.degree = 0

    def fill_value_table(self):
        # vs random
        x_j = self.a
        h = (self.b - self.a) / self.num_of_points
        for j in range(self.num_of_points + 1):
            self.value_table.append([x_j, self.func(x_j)])
            x_j += h

    def fill_diff_table(self):
        diff_k = [x[1] for x in self.value_table]  # f(x_j)
        self.diff_table.append(diff_k[0])
        for k in range(1, self.degree + 1):
            diff_next = []  # f(..k..) -> f (..k + 1..)
            for i in range(self.degree + 1 - k):
                u = diff_k[i + 1] - diff_k[i]
                v = self.value_table[i + k][0] - self.value_table[i][0]
                diff_next.append(u / v)
            diff_k = diff_next
            self.diff_table.append(diff_k[0])

    def take_closest_points(self):
        # sort by distance from x and take first n + 1
        self.value_table = sorted(self.value_table, key=lambda t: abs(t[0] - self.x))
        self.value_table = self.value_table[:self.degree + 1]
        # self.value_table = sorted(self.value_table, key=lambda t: t[0])

    def lagrange_part(self, k, x):
        u = 1
        v = 1
        for i in range(self.degree + 1):
            if i != k:
                u *= (x - self.value_table[i][0])
                v *= (self.value_table[k][0] - self.value_table[i][0])

        return u / v

    def lagrange(self):
        lagrange = 0
        for i in range(self.degree + 1):
            lagrange += self.lagrange_part(i, self.x) * self.func(self.value_table[i][0])
        return lagrange

    def newton(self):
        newton = 0
        term = 1
        for i in range(0, self.degree + 1):
            newton += term * self.diff_table[i]
            term *= (self.x - self.value_table[i][0])
        return newton
    
    def execute(self):
        self.degree = self.input_polynom_degree(self.num_of_points)

        self.value_table = []
        self.fill_value_table()
        tabulate_results(self.value_table, ['x_j', 'f(x_j)'], 'Значения функции в узлах интерполяции')

        self.x = float(input('\nВведите точку интерполирования: '))

        self.take_closest_points()
        tabulate_results(self.value_table, ['x_j', 'f(x_j)'], 'Возьмем ближайшие n + 1 точку к x')

        self.diff_table = []
        self.fill_diff_table()
        tabulate_results(self.diff_table, ['k', 'f(x_0; ...; x_k)'],
                         'Разделенные разности')

        print('\nЗначение многочленов:')

        lagrange = self.lagrange()
        print(f'В форме Лагранжа {lagrange}, погрешность: {abs_error(self.func(self.x), lagrange)}')

        newton = self.newton()
        print(f'В форме Ньютона {newton}, погрешность: {abs_error(self.func(self.x), newton)}')