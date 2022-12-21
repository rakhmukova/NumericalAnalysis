import math

from common.functions import tabulate_results


class MelerFormula:
    def __init__(self, f, N):
        self.f = f
        self.N = N
        self.nodes = []
        self.find_nodes()
        tabulate_results(zip(range(len(self.nodes)), self.nodes), headers=['k', 'x_k'], title=f'Узлы КФ Мелера для N={N}')
        print(f'\nКоэффициент: {self.coefficient()}')

    def find_nodes(self):
        for k in range(self.N):
            arg = (2*(k + 1) - 1) / (2*self.N)
            node = math.cos(arg * math.pi)
            self.nodes.append(node)

    def coefficient(self):
        return math.pi / self.N

    def integrate(self):
        sum_int = sum(map(lambda node: self.f(node), self.nodes))
        return sum_int * self.coefficient()
