from sys import argv


def create_stem_dict(file_name):
    input_file = open(file_name, 'r')

    key = ""
    value = ""

    is_before_semicolumn = True

    dictionary = {}

    for char in input_file.read():
        if char == ':':
            is_before_semicolumn = False
            dictionary[key] = None
            continue
        if char == '\n':
            is_before_semicolumn = True
            dictionary[key] = value
            key = ""
            value = ""
            continue

        if is_before_semicolumn:
            key += char
        else:
            value += char

    input_file.close()
    return dictionary


stem_file = argv[1]
word = argv[2]

dictionary = create_stem_dict(stem_file)

print(dictionary[word])

