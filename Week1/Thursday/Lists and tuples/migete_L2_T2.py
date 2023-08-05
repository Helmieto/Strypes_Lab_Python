import sys
import string

str1 = sys.argv[1]
str2 = sys.argv[2]

l1 = list(str1.lower().replace(" ", ""))
l1.sort()
l2 = list(str2.lower().replace(" ", ""))
l2.sort()


if l1 == l2:
    print("True")

else:
    print("False")