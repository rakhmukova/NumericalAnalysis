from lab1.specify_roots_methods.specify_method import SpecifyMethod


class BisectionMethod(SpecifyMethod):
    def specify_roots(self, ai, bi):
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

    @staticmethod
    def name():
        return 'Метод бисекции'

    @staticmethod
    def results_headers():
        return ['Корень', 'Количество шагов', 'Длина последнего отрезка',
                'Абсолоютная величина невязки']
