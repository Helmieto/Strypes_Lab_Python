import sys


def power(numb, powr):

    if powr == 1:
        return  numb
    else:

        return  power(numb, powr - 1) * numb

print(power(int(sys.argv[1]), int(sys.argv[2])))