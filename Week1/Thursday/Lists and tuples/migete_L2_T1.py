import sys


is_sorted = 1

for i in range(1, len(sys.argv) - 1):

    if sys.argv[i] > sys.argv[i+1]:
        print("unsorted")
        is_sorted = 0
        break

if is_sorted:
    print("sorted")
