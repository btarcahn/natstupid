import unittest

from .artifacts import Board


class BoardInitTest(unittest.TestCase):
    JSON_STRING = '{"white": [[1,5,3],[1,3,4]],"black": [[2,4,6],[1,3,1],[1,5,1]]}'

    def setUp(self):
        self.board_candidate = Board(json_string=
                                     '{"white": [[1,5,3],[1,3,4]],"black": [[2,4,6],[1,3,1],[1,5,1]]}')

    def check_size(self):
        self.assertIsNotNone(self.board_candidate)


if __name__ == "__main__":
    unittest.main()
