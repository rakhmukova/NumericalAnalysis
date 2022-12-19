import math

from common.functions import tabulate_results
from common.integrate import Integration


class MelerIntegration:
    def __init__(self, f, N):
        self.f = f
        self.N = N
        self.nodes = []
        self.find_nodes()
        tabulate_results(zip(range(len(self.nodes)), self.nodes), title=f'Узлы КФ Мелера для N={N}')

    def find_nodes(self):
        for k in range(self.N):
            arg = (2*(k + 1) - 1) / (2*self.N)
            node = math.cos(arg * math.pi)
            self.nodes.append(node)

    def integrate(self):
        sum_int = sum(map(lambda node: self.f(node), self.nodes))
        return sum_int * math.pi / self.N


if __name__ == '__main__':
    def f(x):
        return math.exp(x) * math.sin(x ** 2)
    integartion = Integration(-1, 1, f, lambda x: 1 / math.sqrt(1 - x ** 2))
    precise_value = integartion.precise()
    degrees = input('Введите N1, N2, N3: ').split()
    approximate_values = []
    for degree in degrees:
        meler = MelerIntegration(f, int(degree))
        value = meler.integrate()
        approximate_values.append(value)

    print(f'\nТочное значение: {precise_value}')
    tabulate_results(zip(degrees, approximate_values), title='Приближенные значения интеграла')
