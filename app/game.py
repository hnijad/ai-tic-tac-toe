import numpy as np
from typing import List, Tuple

class Board:
    def __init__(self, size, target) -> None:
        self.size = size
        self.target = target
        self.board = np.array([['-' for _ in range(size)] for _ in range(size)])
        self.empty_squares = self.board
        self.marked_squares = 0
        
    def mark_square(self, row, col, player):
        self.board[row][col] = player
        # self.empty_squares[row][col] = '-'
        self.marked_squares += 1
