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
    
    
class Bot:
    
    def __init__(self, level=0, player=1) -> None:
        self.level = level
        self.player = player
    
    def random_move(self, board) -> Tuple[int, int]:
        empty_squares = board.get_empty_squares()
        random_square = empty_squares[np.random.randint(len(empty_squares))]
        return random_square
    
    def eval(self, board):
        if self.level == 0:
            # make a random move
            move = self.random_move(board)
        
        else:
            # make a move based on the heuristic and minimax algorithm
            pass
        
        return move
    
    
def main():
    
    board = Board(3, 3)
    bot = Bot(0, 1)