import sys

input = []

for i in range(1, len(sys.argv)):
    input += sys.argv[i]

has_repetitions = 0
input.sort()

for i in range(0, len(input) - 1):
    if input[i] == input[i+1]:
        print("True")
        has_repetitions = 1
        break

if not has_repetitions:
    print("False")