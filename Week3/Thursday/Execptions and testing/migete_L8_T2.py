import unittest
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


class ResultTest(unittest.TestCase):

    def testFroot(self):
        self.assertTrue(bisection(1, 2, f) == 1.154)

    def testGPositiveRoot(self):
        self.assertTrue(bisection(1,2, g) == 1.678)

    def testGNegativeRoot(self):
        self.assertTrue(bisection(-1, 0, g) == -0.768)

    def testExecptionRaising(self):
        with self.assertRaises(SameSignException):
            bisection(0, 1, f)


unittest.main()