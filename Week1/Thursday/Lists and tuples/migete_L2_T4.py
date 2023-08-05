import sys

input_list = []
output_list= []

for i in range(1, len(sys.argv)):
    element = sys.argv[i]
    input_list.append(element)


input_list.sort()

for i in range(0, len(input_list)):
    if input_list[i] not in output_list:
        output_list.append(input_list[i])

print(output_list)

