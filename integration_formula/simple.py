from integration_formula.integration import Integration


class Simple(Integration):
    def __init__(self, a, b, f, p):
        super().__init__(a, b, f, p)

    # d = 0
    def left_rectangle(self):
        return self.interval() * self.phi(self.a)

    def right_rectangle(self):
        return self.interval() * self.phi(self.b)

    # d = 1
    def middle_rectangle(self):
        return self.interval() * self.phi(self.middle_point())

    def trapeze(self):
        return (self.interval() / 2) * (self.phi(self.a) + self.phi(self.b))

    # d = 3
    def simpsons(self):
        return (self.interval() / 6) * (self.phi(self.a) + 4 * self.phi(self.middle_point()) + self.phi(self.b))

    def three_eights(self):
        h = self.interval() / 3
        return self.interval() * (1 / 8 * self.phi(self.a) + 3 / 8 * self.phi(self.a + h) + 3 / 8 * self.phi(
            self.a + 2 * h) + 1 / 8 * self.phi(self.b))