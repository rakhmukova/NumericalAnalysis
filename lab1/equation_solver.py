from common.functions import tabulate_results
from lab1.roots_separator import RootsSeparator
from lab1.specify_roots_methods.bisection import BisectionMethod
from lab1.specify_roots_methods.newton import NewtonMethod
from lab1.specify_roots_methods.newton_modified import NewtonModifiedMethod
from lab1.specify_roots_methods.secants import SecantsMethod


class EquationSolver:
    def __init__(self, func, a, b, n, epsilon):
        self.func = func
        self.a = a
        self.b = b
        self.n = n
        self.epsilon = epsilon

    def apply_specify_method(self, method_class, intervals, print_info):
        if print_info:
            print(f'\n\n{method_class.name()}\n')

        method = method_class(self.func, self.epsilon)
        results = []
        for i in range(0, len(intervals)):
            result = method.specify_roots(intervals[i][0], intervals[i][1])
            if result is None:
                continue
            results.append([i] + result)

        if len(results) != len(intervals):
            print('Другие корни нельзя уточнить. Третье условие теоремы о сходимости не выполнено\n')

        if print_info:
            tabulate_results(results, headers=method_class.results_headers())
        return results

    def separate_roots(self, print_info):
        roots_separator = RootsSeparator(self.func, self.a, self.b, self.n)
        if print_info:
            print(f'\n\n{RootsSeparator.name()}\n')
        intervals = roots_separator.separate()
        if print_info:
            tabulate_results(intervals, headers=RootsSeparator.results_headers())
        return intervals

    def specify_roots(self, intervals, print_info):
        specify_method_classes = [
            BisectionMethod,
            NewtonMethod,
            NewtonModifiedMethod,
            SecantsMethod
        ]

        for specify_method_class in specify_method_classes:
            self.apply_specify_method(specify_method_class, intervals, print_info)

    def solve(self, print_info=True):
        intervals = self.separate_roots(print_info)
        self.specify_roots(intervals, print_info)


def find_roots(equation, a, b, N, epsilon, method_name='bisection', print_info=True):
    solver = EquationSolver(equation, a, b, N, epsilon)
    intervals = solver.separate_roots(print_info)

    methods_classes = {
        'bisection': BisectionMethod,
        'newton': NewtonMethod,
        'newton_modified': NewtonModifiedMethod,
        'secant': SecantsMethod
    }

    method_class = methods_classes[method_name]
    method_result = solver.apply_specify_method(method_class, intervals, print_info)
    return [method_result[i][1] for i in range(len(method_result))]