import sys

def fibonacci(range, numbers_list):
    if range == 2:
        return  1

    elif range == 1:
        return 0

    else:
        if len(numbers_list) >= range:
            return  numbers_list[range - 1]

        tba = fibonacci(range - 1, numbers_list) + fibonacci(range - 2, numbers_list)
        numbers_list.append(tba)

        return tba


_from = int(sys.argv[1]) - 1
_to = int(sys.argv[2])

fibonacci_numbers = [0, 1]

fibonacci(_to, fibonacci_numbers)
print(fibonacci_numbers[_from:_to])