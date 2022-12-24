import math

from common.functions import print_lab, execution_loop, input_borders, input_param
from lab1.equation_solver import EquationSolver


if __name__ == '__main__':
    epsilon = math.pow(10, -5)


    def func(x): return 4 * math.cos(x) + 0.3 * x


    print_lab(1, "ЧИСЛЕННЫЕ МЕТОДЫ РЕШЕНИЯ НЕЛИНЕЙНЫХ УРАВНЕНИЙ")
    print(f"Вариант 8. f(x)= 4cos(x) + 0,3x epsilon = {epsilon}")


    def execute():
        a, b = input_borders(-15, 5)
        N = input_param('N', int, 1000)
        epsilon_pow = input_param('степень точности', int, -5)
        epsilon = math.pow(10, epsilon_pow)
        solver = EquationSolver(func, a, b, N, epsilon)
        solver.solve()


    execution_loop(execute)
