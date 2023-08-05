import math
import sys

a= float(sys.argv[1])
b = float(sys.argv[2])
c = float(sys.argv[3])

if a != 0:
   discriminant = b**2 - 4 * a * c

   if discriminant > 0:
       x1 = (-b - math.sqrt(discriminant)) / 2 * a
       x2 = (-b + math.sqrt(discriminant)) / 2 * a
       print(x1, "|", x2)

   elif discriminant == 0:
       x = -b / 2 * a
       print(x)

   else:
       print("No real roots")

else:
    if b != 0:
        x = -c / b
        print(x)
    else:
        print("special case")
