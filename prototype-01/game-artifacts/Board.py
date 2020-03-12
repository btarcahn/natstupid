import json


class Board:
    """Represents the Board in the game."""

    def __init__(self, json_string="", board_size=8):
        """
        Draws a board and initializes all tokens on this board, by
        the directions given in the json string format.
        :param json_string: the json string contains all token positions.
        :param board_size: the size of the square board
        """
        self.__board = [[None for j in range(0, board_size)] for i in range(0, board_size)]

        # Add tokens to the board according to the JSON directions
        json_directions = json.loads(json_string)
        for color in json_directions.keys():
            # Ugh!!!
            pass
