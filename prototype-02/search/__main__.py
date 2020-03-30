import sys
import json

from .artifacts import Board
from .util import print_move, print_boom, print_board


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        test_board = Board(data)
        test_board.print_board()
    # TODO: find and print winning action sequence


if __name__ == '__main__':
    main()
