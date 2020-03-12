from enum import Enum


class TokenColor(Enum):
    """Enumerations of possible colors for the Token"""
    BLACK = 0
    WHITE = 1


class Token:
    """A Token in Expendibots game."""
    __color = TokenColor.BLACK
    x = 0
    y = 0

    def __init__(self, x, y, __color=TokenColor.BLACK):
        self.x = x
        self.y = y
        self.__color = __color
