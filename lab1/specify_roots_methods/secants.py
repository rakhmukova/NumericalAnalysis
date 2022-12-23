from abc import ABC

from lab1.specify_roots_methods.specify_method import SpecifyMethod


class SecantsMethod(SpecifyMethod, ABC):
    def specify_roots(self, ai, bi):
        xi0 = (ai + bi) / 2
        xi1 = ai
        xi2 = bi

        step = 0
        while abs(xi1 - xi2) > self.epsilon:
            xi0, xi1, xi2 = xi1, xi2, xi1 - (self.func(xi1) / (self.func(xi1) - self.func(xi0))) * (xi1 - xi0)
            step += 1

        return [xi2, step, abs(self.func(xi2) - 0)]

    @staticmethod
    def name():
        return 'Метод секущих'

    @staticmethod
    def results_headers():
        return ['Корень', 'Количество шагов',
                'Абсолоютная величина невязки']
