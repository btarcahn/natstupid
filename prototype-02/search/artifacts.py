#!/usr/bin/env python

"""
File: artifacts.py
Contains game artifacts for the Expendibots game.
Note: this file currently follows Python 3.Board.SIZE syntax.
"""

from .util import print_board as util_print_board
from collections import defaultdict
from queue import PriorityQueue
from copy import deepcopy

__author__ = 'Natural Stupidity'
__copyright__ = '© 2020 Natural Stupidity, Expendibots Game'
__version__ = '1.0'
__email__ = 'b.tran17@student.unimelb.edu.au'


class Board:
    """
    Represents a board of the game, technically a 8 x 8 matrix.
    This board supports basic actions as mentioned in the Expendibots
    game, which are: moving horizontally or vertically, and the
    boom action. All of these actions strictly follow the rules
    of the Expendibots game.
    """
    SIZE = 8
    SIZE_INDEX = SIZE - 1

    def __init__(self, data):
        """
        :param data: the dictionary data type.
        """
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
                         message=self.__hash__(),
                         compact=False)

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
            self.board[start_x + dx][start_y] = \
                [self.board[start_x][start_y][0], n]
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
        coords = {'white': [], 'black': []}
        for i in range(0, Board.SIZE_INDEX):
            for j in range(0, Board.SIZE_INDEX):
                if self.board[i][j] is None:
                    pass
                elif self.board[i][j][0] == 'white':
                    coords['white']\
                        .append((self.board[i][j][1], i, j))
                elif self.board[i][j][0] == 'black':
                    coords['black']\
                        .append((self.board[i][j][1], i, j))
        return coords

    def heuristic(self):
        def dist(a, b):
            print(a + '\n')
            print(b + '\n')
            assert a is tuple and b is tuple
            (x1, y1) = a
            (x2, y2) = b
            return abs(x1 - x2) + abs(y1 - y2)
        # TODO compute heuristic function
        pass


class StateNode:
    """
    A graph node that contains a core value (which is
    of type Board), and a list of next nodes. This is
    a recursive data structure.
    """

    def __init__(self, board):
        self.value = board
        self.next_states = []

    def __str__(self) -> str:
        return self.value.__str__()

    def append_next_state(self, next_state):
        """
        Adds a new, adjacent node to this current node.
        This is also known as a graph expansion.
        :param next_state: the next node to be added
        to the list.
        """
        self.next_states.append(next_state)


class ArtificialPlayer:
    """
    An intelligent agent in the game, which has control over
    the Board. A search algorithm is implemented in this agent.
    The agent also has information about the goal state.
    """

    def __init__(self, data):
        self.queue = PriorityQueue()
        self.start_state = StateNode(Board(data))

    @staticmethod
    def goal_function(state):
        """
        Check the state (of StateNode type), and returns True
        if that state is a winning state.
        :param state: the state to be checked.
        """
        assert state is Board
        return state.classify_mark['black'] == []

    @staticmethod
    def get_next_states(current_state):
        """
        Given a current state (which is in StateNode) type,
        finds all next possible states, and attaches them to
        this current state. This is the specific implementation
        of the graph expansion algorithm, in the Expendibots game.
        :param current_state: the current state to be expanded.
        """
        # TODO keep track of previous states! Otherwise, we have cycles.
        assert current_state is StateNode
        next_states = []
        all_whites = current_state.value.classify_mark()['white']
        for white_pos in all_whites:
            # Move in 4 directions, each time create a new state
            for i in range(-white_pos[0], white_pos[0] + 1):
                h_new_state = deepcopy(current_state)
                v_new_state = deepcopy(current_state)
                # TODO further parameterize these statements
                h_new_state.move_horizontally(white_pos[1],
                                              white_pos[2], abs(i), i)
                v_new_state.move_vertically(white_pos[1],
                                            white_pos[2], abs(i), i)
                next_states.append(h_new_state)
                next_states.append(v_new_state)
            # Boom, each time create a new state
            b_new_state = deepcopy(current_state)
            b_new_state.boom(white_pos[1], white_pos[2])
            next_states.append(b_new_state)
        return next_states
