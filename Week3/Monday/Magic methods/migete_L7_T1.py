class Fibs():
    def __init__(self):
        self.iterator = 0
        self.iterator_next = 1
    def __next__(self):
        curr = self.iterator
        self.iterator, self.iterator_next = self.iterator_next, self.iterator_next + 1
        return curr
    def __iter__(self):
        return self
