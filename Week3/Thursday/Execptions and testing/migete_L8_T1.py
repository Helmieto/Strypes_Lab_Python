from math import exp


class SameSignException(Exception):
    pass
def f(x):
    return x ** 3 + 3 * x - 5

def g(x):
    return exp(x)-2*x-2

def bisection(left, right, func):
    mid = (left + right) / 2

    f_left = func(left)
    f_right = func(right)
    f_mid = func(mid)

    if abs(right - left) < 0.001:
        return round(mid, 3)

    if f_mid == 0:
        return mid


    if f_right * f_left  > 0:
        raise SameSignException()

    else:
        if f_mid * f_left < 0:
            return bisection(left, mid, func)
        elif f_mid * f_right < 0:
            return bisection(mid, right, func)


def input_func():
    while True:

        try:
            a = int(input("a="))
            b = int(input("b="))
            result = bisection(a, b, g)

        except SameSignException:
            print("f(a) and f(b) have the same sign! Please input new values.")
        except ValueError:
            print("a and b must be numbers! Please input new values.4")
        else:
            print(result)
            break

