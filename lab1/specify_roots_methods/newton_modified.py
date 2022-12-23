import numpy as np
import scipy.misc as sc

from lab1.specify_roots_methods.newton import NewtonMethod


class NewtonModifiedMethod(NewtonMethod):
    def specify_roots(self, ai, bi):
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

    @staticmethod
    def name():
        return 'Модифицированный метод Ньютона'
