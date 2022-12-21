import math

from common.functions import print_lab, abs_error
from common.integrate import Integration
from integration_formula.meler import MelerFormula

if __name__ == '__main__':
    print_lab(5.2, "Вычисление интегралов при помощи КФ Мелера")
    print(f"Вариант 8. \nf(x)=exp(x) * sin(x^2)\n")
    def f(x):
        return math.exp(x) * math.sin(x ** 2)
    integartion = Integration(-1, 1, f, lambda x: 1 / math.sqrt(1 - x ** 2))
    precise_value = integartion.precise()
    degrees = input('Введите N1, N2, N3: ').split()
    approximate_values = []
    for degree in degrees:
        meler = MelerFormula(f, int(degree))
        value = meler.integrate()
        approximate_values.append(value)

    print(f'\nТочное значение: {precise_value}')
    print('\nПриближенные значения интеграла: ')
    absolute_errors = [abs_error(precise_value, approximate_value) for approximate_value in approximate_values]
    for i in range(len(degrees)):
        print(f'\nN = {degrees[i]}\nзначение: {approximate_values[i]}\nпогрешность: {absolute_errors[i]}')
