import unittest
from model.board import Board

class TestAlgo(unittest.TestCase):
    def test_is_game_finished(self):
        board = Board(3, 3, 1)
        board.make_move(0, 0, 'X')
        board.make_move(1, 1, 'X')
        board.make_move(2, 2, 'X')
        state = board.is_game_finished()
        result = True
        self.assertEqual(state, result)


if __name__ == '__main__':
    unittest.main()