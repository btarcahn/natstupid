#!/usr/bin/env python

"""
File: artifacts.py
Contains game artifacts for the Expendibots game.
Note: this file currently follows Python 3.Board.SIZE syntax.
"""

from .util import print_board as util_print_board
from collections import defaultdict
from math import sqrt
from statistics import mean

__author__ = 'Natural Stupidity'
__copyright__ = '© 2020 Natural Stupidity, Expendibots Game'
__version__ = '1.0'
__email__ = 'b.tran17@student.unimelb.edu.au'


class Board:
    """
    Represents a board of the game, technically a 8 x 8 matrix.
    :param data: the dictionary provided as in __main.py__ file
    """
    SIZE = 8
    SIZE_INDEX = SIZE - 1

    def __init__(self, data):
        self.board = [[None for j in range(0, Board.SIZE)]
                      for i in range(0, Board.SIZE)]
        for pile in data['white']:
            self.board[pile[1]][pile[2]] = ['white', pile[0]]
        for pile in data['black']:
            self.board[pile[1]][pile[2]] = ['black', pile[0]]

    def __str__(self) -> str:
        return self.board.__str__()

    def to_printable_dict(self) -> dict:
        """
        Converts the instance to a dictionary, which
        can then be used in the util.print_board method.
        """
        printable_dict = defaultdict()
        for i in range(0, Board.SIZE):
            for j in range(0, Board.SIZE):
                if self.board[i][j] is not None:
                    printable_dict[(i, j)] = self.board[i][j]
        return printable_dict

    def print_board(self):
        """
        Applies the util.print_board method to the instance.
        """
        util_print_board(board_dict=self.to_printable_dict(),
                         message=str(self.dist_white_to_black()))

    def has_same_color(self, x1, y1, x2, y2):
        """
        Returns true if the two stacks at the given coordinates
        contain pieces having the same color.
        :param x1: the x-coordinate of stack 1.
        :param y1: the y-coordinate of stack 1.
        :param x2: the x-coordinate of stack 2.
        :param y2: the y-coordinate of stack 2.
        """
        color1 = None if self.board[x1][y1] is None \
            else self.board[x1][y1][0]
        color2 = None if self.board[x2][y2] is None \
            else self.board[x2][y2][0]
        return color1 == color2

    def boom(self, start_x, start_y):
        """
        Initiates an EXPLOSION with a starting point.
        :param start_x: the x-coordinate of the starting point
        :param start_y: the y-coordinate of the starting point.
        """

        self.board[start_x][start_y] = None

        # Up, down, left, right corners
        if start_y < Board.SIZE_INDEX \
                and self.board[start_x][start_y + 1] is not None:
            self.boom(start_x, start_y + 1)
        if start_y > 0 and self.board[start_x][start_y - 1] is not None:
            self.boom(start_x, start_y - 1)
        if start_x > 0 and self.board[start_x - 1][start_y] is not None:
            self.boom(start_x - 1, start_y)
        if start_x < Board.SIZE_INDEX \
                and self.board[start_x + 1][start_y] is not None:
            self.boom(start_x + 1, start_y)

        # Diagonal corners
        if start_x > 0 and start_y > 0 \
                and self.board[start_x - 1][start_y - 1] is not None:
            self.boom(start_x - 1, start_y - 1)
        if start_x < Board.SIZE_INDEX and start_y < Board.SIZE_INDEX \
                and self.board[start_x + 1][start_y + 1] is not None:
            self.boom(start_x + 1, start_y + 1)
        if start_x > 0 and start_y < Board.SIZE_INDEX \
                and self.board[start_x - 1][start_y + 1] is not None:
            self.boom(start_x - 1, start_y + 1)
        if start_x < 0 and start_y > Board.SIZE_INDEX \
                and self.board[start_x + 1][start_y - 1] is not None:
            self.boom(start_x + 1, start_y - 1)

    def move_horizontally(self, start_x, start_y, n, dx):
        """
        Moves pieces currently in the place of origin, horizontally.
        This movement follows the rules in Expendibots. An exception
        is thrown if any of these rules is violated.

        :param start_x: the x-coordinate of the place of origin.
        :param start_y: the y-coordinate of the place of origin.
        :param n: number of pieces to be moved.
        :param dx: the horizontal displacement.
        """
        if self.board[start_x][start_y] is None or dx == 0 or n <= 0:
            return

        # Check if the movement is doable
        if self.board[start_x][start_y][1] < abs(dx):
            raise IndexError('Insufficient pieces to perform movement.')
        if not start_x + dx in range(0, Board.SIZE):
            raise IndexError('Invalid movement (out of board).')

        # Destination found
        if self.board[start_x + dx][start_y] is None:
            self.board[start_x + dx][start_y] = [self.board[start_x][start_y][0], n]
            self.board[start_x][start_y][1] -= n
            if self.board[start_x][start_y][1] == 0:
                self.board[start_x][start_y] = None
        elif self.has_same_color(start_x, start_y, start_x + dx, start_y):
            self.board[start_x + dx][start_y][1] += n
            self.board[start_x][start_y][1] -= n
            if self.board[start_x][start_y][1] == 0:
                self.board[start_x][start_y] = None
        else:
            raise IndexError('Invalid movemnet (opponent is present).')

    def move_vertically(self, start_x, start_y, n, dy):
        """
        Moves pieces currently in the place of origin, vertically.
        This movement follows the rules in Expendibots. An exception
        is thrown if any of these rules is violated.

        :param start_x: the x-coordinate of the place of origin.
        :param start_y: the y-coordinate of the place of origin.
        :param n: number of pieces to be moved.
        :param dy: the vertical displacement.
        """
        if self.board[start_x][start_y] is None or dy == 0 or n <= 0:
            return

        # Check if the movement is doable
        if self.board[start_x][start_y][1] < abs(dy):
            raise IndexError('Insufficient pieces to perform movement.')
        if not start_y + dy in range(0, Board.SIZE):
            raise IndexError('Invalid movement (out of board).')

        # Destination found
        if self.board[start_x][start_y + dy] is None:
            self.board[start_x][start_y + dy] = [self.board[start_x][start_y][0], n]
            self.board[start_x][start_y][1] -= n
            if self.board[start_x][start_y][1] == 0:
                self.board[start_x][start_y] = None
        elif self.has_same_color(start_x, start_y, start_x, start_y + dy):
            self.board[start_x][start_y + dy][1] += n
            self.board[start_x][start_y][1] -= n
            if self.board[start_x][start_y][1] == 0:
                self.board[start_x][start_y] = None
        else:
            raise IndexError('Invalid movement (opponent is present).')

    def classify_mark(self) -> dict:
        coords = defaultdict()
        for i in range(0, Board.SIZE_INDEX):
            for j in range(0, Board.SIZE_INDEX):
                if self.board[i][j] is None:
                    pass
                elif self.board[i][j][0] == 'white':
                    coords['white'] = (i, j)
                elif self.board[i][j][0] == 'black':
                    coords['black'] = (i, j)
        return coords

    def dist_white_to_black(self):
        # TODO have not test/documented this function
        # TODO Probably it's wrong...
        def dist(a, b):
            assert a is tuple and b is tuple
            (x, y) = a
            (u, v) = b
            return sqrt((x - u) ** 2 + (y - v) ** 2)

        return mean(map(lambda x, y: dist(x, y),
                        self.classify_mark().get('white'),
                        self.classify_mark().get('black')))
