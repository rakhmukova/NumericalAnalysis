from abc import abstractmethod


class SpecifyMethod:
    def __init__(self, func, epsilon):
        self.func = func
        self.epsilon = epsilon

    @abstractmethod
    def specify_roots(self, ai, bi):
        pass

    @staticmethod
    @abstractmethod
    def name():
        pass

    @staticmethod
    @abstractmethod
    def results_headers():
        pass
