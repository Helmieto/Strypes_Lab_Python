import sys

searched_value = sys.argv[1]

d={1:'a',2:'b',3:'c',4:'a',5:'d',6:'e',7:'a',8:'b'}

output_list = []
for i in d.keys():
    if d[i] == searched_value:
        output_list.append(i)

print(output_list)