from sys import argv
input_file = argv[1]
output_file = argv[2]

f = open(input_file, 'r')

lines = f.readlines()

f.close()

lines.sort()

g = open(output_file, 'x+')

for line in lines:
    if line[-1] != '\n':
        line += '\n'
    g.write(line)

g.close()