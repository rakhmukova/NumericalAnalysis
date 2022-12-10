import math

from common.main import print_lab
from lab4_1.integrate import Integration

if __name__ == '__main__':
    def f(x):
        return math.exp(x)

    print_lab(4.2, 'Приближённое вычисление интеграла по квадратурным формулам')
    print(f"Вариант 8. \nf(x)=e^x\n")

    a = int(input("Введите левый предел интегрирования: "))
    b = int(input("Введите правый предел интегрирования: "))

    def p(x): return 1

    integration = Integration(a, b, f, p)
    precise_value = integration.precise()
    print(f"Точное значение интеграла: {precise_value}\n")

    methods_and_names = [
        (integration.left_rectangle, "левого прямоугольника"),
        (integration.right_rectangle, "правого прямоугольника"),
        (integration.middle_rectangle, "среднего прямоугольника"),
        (integration.trapeze, "трапеции"),
        (integration.simpsons, "Симпсона (или парабол)"),
        (integration.three_eights, "3/8"),
    ]

    for methods_and_name in methods_and_names:
        method, name = methods_and_name
        approximate_value = method()
        print(f"КФ {name} : {approximate_value}")
        print(f"Абсолютная погрешность: {abs(precise_value - float(approximate_value))}\n")
