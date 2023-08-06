import sys

input_text = list(sys.argv[1])
input_text.sort()

histogram = {}

for i in range(0, len(input_text)):
    if input_text[i] in histogram.keys():
        histogram[input_text[i]] += 1
    else:
        histogram[input_text[i]]=1

print(histogram)
