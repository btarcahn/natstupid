class Stack:
    """Lightweight representation of a stack data structure.
    Reference: https://runestone.academy/runestone/books/published/pythonds/BasicDS/ImplementingaStackinPython.html
    """
    def __init__(self):
        self.__items = []

    def is_empty(self):
        return self.__items == []

    def push(self, item):
        return self.__items.insert(0, item)

    def pop(self):
        return self.__items.pop(0) if self.is_empty() else None

    def peek(self):
        return self.__items[0] if self.is_empty() else None

    def size(self):
        return len(self.__items)
