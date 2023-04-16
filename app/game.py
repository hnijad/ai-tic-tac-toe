import numpy as np
from typing import List, Tuple

class Board:
    def __init__(self, size, target) -> None:
        self.size = size
        self.target = target
        self.squares = np.array([['-' for _ in range(size)] for _ in range(size)])
        self.empty_squares = self.squares
        self.marked_squares = 0
        
    def mark_square(self, row, col, player):
        self.board[row][col] = player
        # self.empty_squares[row][col] = '-'
        self.marked_squares += 1
    
    def check_win(self, player):
        # Check rows
        n = self.size
        m = self.target
        grid = self.squares
        
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
        return np.argwhere(self.squares == '-')
        
    def is_empty_square(self, row, col):
        return self.squares[row][col] == '-'
    
    def is_board_full(self):
        return self.marked_squares == self.size**2
    
    def is_board_empty(self):
        return self.marked_squares == 0
        
    def print_board(self):
        for row in self.squares:
            print(row)
            
class Bot:
    
    def __init__(self, level: int=0, player: str='O') -> None:
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
    # grid = board.squares
    board.print_board()
    bot = Bot(0, 'O')
    
    while True:
        num1, num2 = map(int, input("Enter two space-separated integers: ").split())
        
        if not board.is_empty_square(num1, num2):
            print("Invalid move")
            continue
        
        board.mark_square(num1, num2, 'X')
        board.print_board()

        print(">>> Bot's turn: ")

        x, y = bot.eval(board)
        # if x == -1:
        #     sys.exit(0)
        
        board.mark_square(x, y, 'O')
        board.print_board()
    
    row_id, col_id = bot.eval(board)
    
if __name__ == '__main__':
    main()
    