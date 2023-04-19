import unittest
from unittest import TestCase

from app.model.board import Board


class TestBoard(TestCase):
    def test_is_game_finished(self):
        # given
        board = Board(size=3, target=3, turn=1)
        board.make_move(0, 0, 'X')
        board.make_move(1, 1, 'X')
        board.make_move(2, 2, 'X')

        # when
        res = board.is_game_finished()

        # then
        self.assertTrue(res)

    def test_make_move(self):
        # given
        board = Board(4, 2, 1)
        actual = [['-', 'X', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']]

        # when
        board.make_move(0, 1, 'X')

        # then
        self.assertEqual(board.state, actual)

    def test_reset_move(self):
        # given
        board = Board(4, 2, 1)
        board.make_move(0, 1, 'X')
        actual = [['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-'], ['-', '-', '-', '-']]

        # when
        board.reset_move(0, 1)

        # then
        self.assertEqual(board.state, actual)

    def test_get_possible_moves(self):
        # given
        board = Board(size=3, target=3, turn=1)
        board.make_move(0, 0, 'X')
        actual = [(0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

        # when
        res = board.get_possible_moves()

        # then
        self.assertEqual(len(res), len(actual))
        self.assertEqual(res, actual)

    def test_get_mark(self):
        # given
        board = Board(size=3, target=3, turn=1)

        # when
        res = board.get_mark()

        # then
        self.assertEqual(res, 'O')

    def test_get_opponent_mark(self):
        # given
        board = Board(size=3, target=3, turn=1)

        # when
        res = board.get_opponent_mark()

        # then
        self.assertEqual(res, 'X')

    def test_count_moves(self):
        # given
        board = Board(size=3, target=3, turn=1)
        board.make_move(0, 0, 'X')
        board.make_move(1, 1, 'O')
        board.make_move(2, 2, 'O')

        # when
        res = board.count_moves()

        # then
        self.assertEqual(res, 3)

if __name__ == '__main__':
    unittest.main()
