import sys
import json

from .artifacts import ArtificialPlayer


def main():
    with open(sys.argv[1]) as file:
        data = json.load(file)
        player = ArtificialPlayer(data)
        # print("# From this state, there are "
        #       + str(player.get_next_states(player.start_state).__len__())
        #       + " posible next states.")

    # Apply iterative deepening search
    player.start_searching()


if __name__ == '__main__':
    main()
