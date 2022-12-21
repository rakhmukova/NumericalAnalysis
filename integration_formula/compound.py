import scipy

from integration_formula.integration import Integration


class Compound(Integration):

    def __init__(self, a, b, f, p, m, ders):
        super().__init__(a, b, f, p)
        self.func_maximums = []
        self.find_max(ders)
        self.m = m
        self.h = self.interval() / self.m

    # 2 (f(A + h) + ... + f(B-h))
    def __double_part(self):
        result = 0
        x = self.a + self.h
        for i in range(self.m - 1):
            result += self.f(x)
            x += self.h
        return 2 * result

    def __sum_of_ends(self):
        return self.f(self.a) + self.f(self.b)

    def __middle_part(self):
        result = 0
        x = self.a + self.h / 2
        for i in range(self.m):
            result += self.f(x)
            x += self.h
        return result

    def left_rectangles(self):
        result = 0
        x = self.a
        for i in range(self.m):
            result += self.f(x)
            x += self.h
        return result * self.h

    def right_rectangles(self):
        result = 0
        x = self.a
        for i in range(self.m):
            x += self.h
            result += self.f(x)
        return result * self.h

    def middle_rectangles(self):
        return self.__middle_part() * self.h

    def trapezes(self):
        result = self.__double_part() + self.__sum_of_ends()
        return (result * self.h) / 2

    def simpsons_multiple(self):
        result = self.__sum_of_ends() + self.__double_part() + self.__middle_part() * 4
        return (result * self.h) / 6

    def find_max(self, ders):
        if ders is None:
            return
        for i in range(4):
            func_max = scipy.optimize.minimize_scalar(lambda x: -ders[i](x), bounds=[self.a, self.b],
                                                      method='bounded')
            self.func_maximums.append(-func_max['fun'])

    def theoretical_error(self, method):
        algebraic_precision_and_const_value = {
            self.left_rectangles: [0, 1 / 2],
            self.right_rectangles: [0, 1 / 2],
            self.middle_rectangles: [1, 1 / 24],
            self.trapezes: [1, 1 / 12],
            self.simpsons_multiple: [3, 1 / 2880]
        }

        d, value = algebraic_precision_and_const_value[method]
        func_max = self.func_maximums[d]
        return value * func_max * self.interval() * self.h ** (d + 1)
