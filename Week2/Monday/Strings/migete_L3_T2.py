import sys

message = sys.argv[1].lower()
key = sys.argv[2].lower()

counter = 0
key_length = len(key)
new_message = ""

for i in range(0, len(message)):
    if not message[i].isalpha():
        new_message += message[i]
        continue
    offset = ord(key[counter % key_length]) - ord('a')
    counter +=1
    new_char = chr(ord('a') + ((ord(message[i]) - ord('a') + offset) % 26))
    new_message += new_char

print(new_message)

