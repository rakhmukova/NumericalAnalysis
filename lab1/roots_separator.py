
class RootsSeparator:
    def __init__(self, func, a, b, n):
        self.func = func
        self.a = a
        self.b = b
        self.n = n
        
    def separate(self):
        h = (self.b - self.a) / self.n
        x1 = self.a
        x2 = self.a + h
        y1 = self.func(x1)
        intervals = []
        for i in range(self.n):
            y2 = self.func(x2)
            if y1 * y2 <= 0:
                intervals.append((x1, x2))
            x1 += h
            x2 += h
            y1 = y2

        return intervals

    @staticmethod
    def name():
        return 'Отделение корней'

    @staticmethod
    def results_headers():
        return ['Интервал']