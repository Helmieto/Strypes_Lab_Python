import sys

def check_palindrome(str, begin, end):
    if begin == end:
        return True

    if str[begin] == str[end]:
        return check_palindrome(str, begin + 1, end  -1)
    else:
        return False



str = sys.argv[1]

print(check_palindrome(str, 0, len(str) - 1))
