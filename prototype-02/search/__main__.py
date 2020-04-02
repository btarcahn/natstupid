import sys
import json

from .artifacts import Board, ArtificialPlayer
from .util import print_move, print_boom, print_board


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        test_board = Board(data)
        test_board.print_board()
        player = ArtificialPlayer(data)
        print("From this state, there are "
              + str(player.get_next_states(player.start_state).__len__())
              + " posible next states.")
        player.expand_graph()
    # TODO: find and print winning action sequence


if __name__ == '__main__':
    main()
