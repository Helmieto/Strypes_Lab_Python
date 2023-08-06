import sys

message=sys.argv[1].lower()
key = int(sys.argv[2])

new_message = ""

for i in range(0, len(message)):
    if not message[i].isalpha():
        new_message += message[i]
        continue

    new_char = chr(ord('a') + ((ord(message[i]) - ord('a') + key) % 26))
    new_message += new_char

print(new_message)

