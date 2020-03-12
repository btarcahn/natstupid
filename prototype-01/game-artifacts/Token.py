from enum import Enum


class TokenColor(Enum):
    """Enumerations of possible colors for the Token"""
    BLACK = 0
    WHITE = 1


class Token:
    """A Token in Expendibots game."""

    def __init__(self, x, y, __color=TokenColor.BLACK):
        self.x = x
        self.y = y
        self.__color = __color
