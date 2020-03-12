class Board:
    """Represents the Board in the game."""

    def __init__(self, m=0, n=0):
        __x_size = m if m > 0 else 0
        __y_size = n if n > 0 else m
        self.__board = [[None for j in range(0, n)] for i in range(0, m)]