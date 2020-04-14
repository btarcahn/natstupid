import sys
import json

from .artifacts import ArtificialPlayer


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        player = ArtificialPlayer(data)
        print("From this state, there are "
              + str(player.get_next_states(player.start_state).__len__())
              + " posible next states.")
        # player.expand_graph()
        player.ids_control()
    # TODO: find and print winning action sequence


if __name__ == '__main__':
    main()
