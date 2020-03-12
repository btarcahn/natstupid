import json
from enum import Enum


class Stack:
    """Lightweight representation of a stack data structure.
    Reference: https://runestone.academy/runestone/books/published/pythonds/BasicDS/ImplementingaStackinPython.html
    """
    def __init__(self, n=0):
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



class Board:
    """Represents the Board in the game."""

    def __init__(self, json_string="", board_size=8):
        """
        Draws a board and initializes all tokens on this board, by
        the directions given in the json string format.
        :param json_string: the json string contains all token positions.
        :param board_size: the size of the square board
        """
        self.__board = [[Stack() for j in range(0, board_size)] for i in range(0, board_size)]

        # Add tokens to the board according to the JSON directions
        # Format: [n_items, x_coords, y_coords]
        json_directions = json.loads(json_string)
        for color in json_directions.keys():
            color_code = TokenColor.enumerate_string(color)
            for direction in json_directions[color]:
                for i in range(0, direction[0]):
                    self.__board[direction[1]][direction[2]].push(TokenColor.enumerate_string(color_code))
