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

    @staticmethod
    def apply_specify_method(method, intervals):
        results = []
        for i in range(0, len(intervals)):
            result = method.specify_roots(intervals[i][0], intervals[i][1])
            if result is None:
                continue
            results.append([i] + result)

        if len(results) != len(intervals):
            print('Другие корни нельзя уточнить. Третье условие теоремы о сходимости не выполнено\n')
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
            specify_method = specify_method_class(self.func, self.epsilon)
            if print_info:
                print(f'\n\n{specify_method_class.name()}\n')
            specify_results = self.apply_specify_method(specify_method, intervals)
            if print_info:
                tabulate_results(specify_results, headers=specify_method_class.results_headers())

    def solve(self, print_info=True):
        intervals = self.separate_roots(print_info)
        self.specify_roots(intervals, print_info)
