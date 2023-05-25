print("Введите коэффициенты a,b,c квадратного уравнения ax^2 + bx + c = 0:")
a = float(input("a = "))
b = float(input("b = "))
c = float(input("c = "))
if a != 0:
    d = b ** 2 - 4 * a * c
    if d > 0:
        x1 = ((-1) * b + d ** (1/2)) / (2 * a)
        x2 = ((-1) * b - d ** (1/2)) / (2 * a)
        print("Два корня: \n  x1 = %.2f \n  x2 = %.2f" % (x1, x2))
    elif d == 0:
        x = (-1) * b / (2 * a)
        print("Один корень: \n  x = %.2f" % x)
    else:
        print("Корней нет.")
else:
    print("Уравнение не является квадратным.")