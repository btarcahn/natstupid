from enum import Enum


class TokenColor(Enum):
    """Enumerations of possible colors for the Token"""

    # TODO this class may be more concise?
    BLACK = 0
    WHITE = 1

    @staticmethod
    def enumerate_string(str):
        if str.lower() == "black":
            return TokenColor.BLACK
        elif str.lower() == "white":
            return TokenColor.WHITE


class Token:
    """A Token in Expendibots game."""

    def __init__(self, x, y, __color=TokenColor.BLACK):
        self.x = x
        self.y = y
        self.__color = __color
