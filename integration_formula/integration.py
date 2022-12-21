
class Integration:

    def __init__(self, a, b, f, p):
        self.a = a
        self.b = b
        self.f = f
        self.p = p

    def phi(self, x):
        return self.p(x) * self.f(x)

    def interval(self):
        return self.b - self.a

    def middle_point(self):
        return (self.b + self.a) / 2