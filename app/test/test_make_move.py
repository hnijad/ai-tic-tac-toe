import unittest
from model.board import Board

class TestAlgo(unittest.TestCase):
    def test_make_move(self):
        board = Board(4, 2, 1)
        result = [['-', 'X', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']]
        board.make_move(0, 1, 'X')
        new_state = board.state
        self.assertEqual(new_state, result)


if __name__ == '__main__':
    unittest.main()