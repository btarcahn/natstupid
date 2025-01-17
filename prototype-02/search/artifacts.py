#!/usr/bin/env python

"""
File: artifacts.py
Contains game artifacts for the Expendibots game.
Note: this file currently follows Python 3.7 syntax.
"""

from .util import print_board as util_print_board
from collections import defaultdict, deque
from copy import deepcopy
from sys import setrecursionlimit
from math import sqrt

__author__ = 'Natural Stupidity'
__copyright__ = '© 2020 Natural Stupidity, Expendibots Game'
__version__ = '1.0'
__email__ = 'b.tran17@student.unimelb.edu.au'

setrecursionlimit(10000)


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

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Board) and \
               self.board.__eq__(o.board)

    def __ne__(self, o: object) -> bool:
        if not isinstance(o, Board):
            return True
        return self.board.__ne__(o.board)

    def __hash__(self) -> int:
        return str(self.board).__hash__()

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
        An explosion (or boom action) follows the rules of
        the Expendibots game.
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

    def classify_mark(self, num_of_pieces=True) -> dict:
        """
        Returns a dictionary consisting 2 keys: 'black', and 'white'.
        The value is a list of 2-tuples (x,y) of the piece sitting on
        that coordinate.
        The values are 2 lists of tuple contains the following:
        (number_of_pieces, x_coord, y_coord) if num_of_pieces is False.
        (x_coord, y_coord) if num_of_pieces is True.
        :param num_of_pieces: whether number_of_pieces component should
        be added to the tuple.
        """
        coords = {'white': [], 'black': []}
        if num_of_pieces:
            for i in range(0, Board.SIZE):
                for j in range(0, Board.SIZE):
                    if self.board[i][j] is None:
                        pass
                    elif self.board[i][j][0] == 'white':
                        coords['white'] \
                            .append((self.board[i][j][1], i, j))
                    elif self.board[i][j][0] == 'black':
                        coords['black'] \
                            .append((self.board[i][j][1], i, j))
        else:
            for i in range(0, Board.SIZE):
                for j in range(0, Board.SIZE):
                    if self.board[i][j] is None:
                        pass
                    elif self.board[i][j][0] == 'white':
                        coords['white'].append((i, j))
                    elif self.board[i][j][0] == 'black':
                        coords['black'].append((i, j))
        return coords


class DistTools:
    """
    Quick static methods calculating simple distances
    on a 2D surface.
    """
    @staticmethod
    def manhattan(a: tuple, b: tuple):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def euclidean(a: tuple, b: tuple):
        (x1, y1) = a
        (x2, y2) = b
        return sqrt((x1 - x2)**2 + (y1 - y2)**2)


class Action:
    """
    Abstract class of a possible action that can be
    applied to a Board. An object of this class
    encapsulates the information on when the Player
    makes a move (BOOM, or MOVE).
    """
    pass


class Move(Action):
    """
    Encapsulates a MOVE action. To use this class, one must
    supply two 2-tuples: origin=(x1,y1) and destination=(x2,y2).
    """

    def __init__(self, n, origin: tuple, destination: tuple):
        self.n = n
        self.origin = origin
        self.destination = destination

    def __str__(self):
        return "MOVE {} from {} to {}.".format(self.n, self.origin, self.destination)


class Boom(Action):
    """
    Encapsulates a BOOM action. To use this class, one must
    supple one 2-tuples: origin=(x,y).
    """

    def __init__(self, origin: tuple):
        self.origin = origin

    def __str__(self) -> str:
        return "BOOM at {}.".format(self.origin)


class StateNode:
    """
    A graph node that contains a core value (which is
    of type Board), and a list of adjacent nodes.
    """

    def __init__(self, board: Board, action_taken: Action):
        self.value = board
        self.action_taken = action_taken
        self.next_states = set()

    def __str__(self) -> str:
        return self.value.__str__()

    def __eq__(self, o: object) -> bool:
        return isinstance(o, StateNode) \
               and self.value.__eq__(o.value)

    def __ne__(self, o: object) -> bool:
        if not isinstance(o, StateNode):
            return True
        return self.value.__ne__(o.value)

    def __hash__(self) -> int:
        return self.value.__hash__()


class ArtificialPlayer:
    """
    An intelligent agent in the game, which has control over
    the Board. A search algorithm is implemented in this agent.
    The agent also has information about the goal state.
    """

    def __init__(self, data):
        self.stack = deque()
        self.start_state = StateNode(Board(data), None)
        self.known_states = set()
        self.max_depth = 0

    @staticmethod
    def goal_function(state: StateNode):
        """
        Check the state (of StateNode type), and returns True
        if that state is a winning state.
        :param state: the state to be checked.
        """
        return state.value.classify_mark().get('black') == []

    @staticmethod
    def get_next_states(current_state: StateNode):
        """
        Determines all possible next states from a current state,
        by applying the moving rules of the Expendibots game. This
        includes moving the pieces up, down, left, right, and
        performing any possible boom action. This is a static method,
        therefore does NOT keep track of any previous states.
        :param current_state: the current state to be expanded.
        """
        next_states = set()
        all_whites = current_state.value.classify_mark()['white']
        for white_pos in all_whites:
            # Move in 4 directions, each time create a new state
            for i in range(1, white_pos[0] + 1):
                for j in range(-white_pos[0], white_pos[0] + 1):
                    h_new_state = deepcopy(current_state.value)
                    v_new_state = deepcopy(current_state.value)
                    try:
                        h_new_state.move_horizontally(white_pos[1],
                                                      white_pos[2], abs(i), j)
                    except IndexError:
                        pass
                    try:
                        v_new_state.move_vertically(white_pos[1],
                                                    white_pos[2], abs(i), j)
                    except IndexError:
                        pass
                    if h_new_state != current_state.value:
                        next_states.add(StateNode(h_new_state,
                                                  Move(i,
                                                       (white_pos[1], white_pos[2]),
                                                       (white_pos[1] + j, white_pos[2]))))
                    if v_new_state != current_state.value:
                        next_states.add(StateNode(v_new_state,
                                                  Move(i,
                                                       (white_pos[1], white_pos[2]),
                                                       (white_pos[1], white_pos[2] + j))))

            # Boom, each time create a new state
            b_new_state = deepcopy(current_state.value)
            b_new_state.boom(white_pos[1], white_pos[2])
            next_states.add(StateNode(b_new_state, Boom((white_pos[1], white_pos[2]))))
        return next_states

    @staticmethod
    def heuristic(state: StateNode):
        """
        Calculates the heuristic of a given state.
        Formula: sum(total_whites_on_that_coord *
                sum(manhattan_dist_to_all_blacks))
        """
        total = 0
        coords = state.value.classify_mark()
        for white in coords['white']:
            for black in coords['black']:
                total += white[0] * DistTools.manhattan((white[1], white[2]), (black[1], black[2]))
        return total

    def __ids__(self, current_node: StateNode, going_deeper, threshold):
        """
        The implementation of the iterative deepening depth first search,
        with a simple heuristic supplied from the environment.
        :param current_node: the node where the algorithm starts.
        :param going_deeper: the cut-off depth remaining, the search stops
        when this parameter reaches zero.
        :param threshold: the heuristic value, any node that has the heuristic
        value greater than the threshold is ignored.
        """

        # Goal reached, add final step to the stack.
        if self.goal_function(current_node):
            self.stack.append(current_node.action_taken)
            return True

        # Depth cut-off reached, or moving too faraway from the black pieces.
        if going_deeper <= 0 or self.heuristic(current_node) > threshold:
            return False

        # Not there yet, expanding next possible states and reduce
        # the threshold (heuristic value)
        current_node.next_states = self.get_next_states(current_node)
        new_threshold = self.heuristic(current_node)

        # Deepening the search algorithm
        for next_state in current_node.next_states:
            if self.__ids__(next_state, going_deeper - 1, new_threshold):
                self.stack.append(current_node.action_taken)
                # print(current_node.action_taken)
                return True
        return False

    def start_searching(self, max_depth=250):
        """
        Initialize the search algorithm implemented in the
        Artificial Player. The maximum depth for this search
        is set to 250 by default.
        :param max_depth: the maximum depth allowed. If this
        depth is reached, the search will stop, and assume
        that the goal is unreachable.
        """
        depth = 0
        threshold = self.heuristic(self.start_state)
        while self.__ids__(self.start_state, depth, threshold) is False:
            depth += 1
            if depth > max_depth:
                print('Maximum depth of {} exceeded. Assume failure.'.format(max_depth))
                break
        if self.stack:
            self.stack.pop()
        while self.stack:
            print(self.stack.pop())
