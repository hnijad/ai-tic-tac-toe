import unittest
from model.board import Board

class TestAlgo(unittest.TestCase):
    def test_get_possible_moves(self):
        board = Board(3, 3, 0)
        board.make_move(0, 0, 'X')
        possible_moves = board.get_possible_moves()
        result = [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        self.assertEqual(possible_moves, result)


if __name__ == '__main__':
    unittest.main()