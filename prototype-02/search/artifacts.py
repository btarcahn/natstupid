#!/usr/bin/env python

"""
File: artifacts.py
Contains game artifacts for the Expendibots game.
Note: this file currently follows Python 3.7 syntax.
"""

from .util import print_board as util_print_board
from collections import defaultdict

__author__ = 'Natural Stupidity'
__copyright__ = '© 2020 Natural Stupidity, Expendibots Game'
__version__ = '1.0'
__email__ = 'b.tran17@student.unimelb.edu.au'


class Board:
    """
    Represents a board of the game, technically a 8 x 8 matrix.
    :param data: the dictionary provided as in __main.py__ file
    """
    def __init__(self, data):
        self.board = [[[None, 0] for j in range(0, 7)] for i in range(0, 7)]
        whites = data['white']
        blacks = data['black']
        for pile in whites:
            self.board[pile[1]][pile[2]] = ['white', pile[0]]
        for pile in blacks:
            self.board[pile[1]][pile[2]] = ['black', pile[0]]

    def __str__(self) -> str:
        return self.board.__str__()

    def to_printable_dict(self) -> dict:
        """
        Converts the instance to a dictionary, which
        can then be used in the util.print_board method.
        """
        printable_dict = defaultdict()
        for i in range(0, 7):
            for j in range(0, 7):
                if self.board[i][j][0] is not None:
                    printable_dict[(i, j)] = self.board[i][j]
        return printable_dict

    def print_board(self):
        """
        Applies the util.print_board method to the instance.
        """
        util_print_board(board_dict=self.to_printable_dict(),
                         message="instance")

    def boom(self, start_x, start_y):
        """
        Initiates an EXPLOSION with a starting point.
        :param start_x: the x-coordinate of the starting point
        :param start_y: the y-coordinate of the starting point.
        """
        self.board[start_x][start_y] = [None, 0]
        if 0 < start_x < 7 and 0 < start_y < 7:
            self.boom(start_x+1, y)
            self.boom(start_x-1, y)
            self.boom(start_x, y+1)
            self.boom(start_x, y-1)
            self.boom(start_x+1, start_y+1)
            self.boom(start_x-1, start_y-1)
            self.boom(start_x+1, start_y-1)
            self.boom(start_x-1, start_y+1)
        # TODO enumerate other cases
