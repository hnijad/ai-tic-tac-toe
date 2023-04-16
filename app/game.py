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
    
    def check_win(self, player):
        # Check rows
        n = self.size
        m = self.target
        grid = self.board
        
        for i in range(n):
            for j in range(n):
                # Check rows
                if j <= n - m:
                    player_score_row = [grid[i][j+k] == player for k in range(m)]
                    if sum(player_score_row) == m:
                        return True
                        
                # Check columns
                if i <= n - m:
                    player_score_col = [grid[i+k][j] == player for k in range(m)]
                    if sum(player_score_col) == m:
                        return True
                        
                # Check diagonal (top-left to bottom-right)
                if i <= n - m and j <= n - m:
                    player_score_diag_tl_br = [grid[i+k][j+k] == player for k in range(m)]
                    if sum(player_score_diag_tl_br) == m:
                        return True
                        
                # Check diagonal (bottom-left to top-right)
                if i >= m-1 and j <= n - m:
                    player_score_diag_bl_tr = [grid[i-k][j+k] == player for k in range(m)]
                    if sum(player_score_diag_bl_tr) == m:
                        return True
                    
        return False
    
    def get_empty_squares(self):    
        return np.argwhere(self.board == '-')
        
    def is_empty_square(self, row, col):
        return self.board[row][col] == '-'
    
    def is_board_full(self):
        return self.marked_squares == self.size**2
    
    def is_board_empty(self):
        return self.marked_squares == 0
    
 