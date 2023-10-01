class Fibs():
    def __init__(self):
        self.iterator = 0
        self.iterator_next = 1

    def __next__(self):
        temp = self.iterator
        self.iterator = self.iterator_next
        self.iterator_next += temp
        return temp
    def __iter__(self):
        return self


fib = Fibs()

for i in fib:
    if i > 100:
        break
    print(i)
