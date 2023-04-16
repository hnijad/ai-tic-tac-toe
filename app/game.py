import copy
import time
import numpy as np
from typing import List, Tuple

class Board:
    def __init__(self, size, target) -> None:
        self.size = size
        self.target = target
        self.squares = np.array([[0 for _ in range(size)] for _ in range(size)])
        self.empty_squares = np.zeros((size, size), dtype=int)
        self.marked_squares = 0
        
    def mark_square(self, row, col, player_mark):
        self.squares[row][col] = player_mark
        # self.empty_squares[row][col] = '-'
        self.marked_squares += 1
    
    def check_win(self):
        # Check rows
        n = self.size
        m = self.target
        grid = self.squares.copy()
        # print(grid)
        # turn the board into a numeric array
        # print(grid == 'O')
        
        # grid[grid == 'X'] = '1'
        # grid[grid == 'O'] = '-1'
        # print(grid)
        # grid[grid == '-'] = '0'
        
        # grid = grid.astype(int)
        
        for i in range(n):
            for j in range(n):
                # Check rows
                if j <= n - m:
                    score_row = [grid[i][j+k] for k in range(m)]
                    # print(f"score_row: {score_row}")
                    if sum(score_row) == m:
                        return 1
                    elif sum(score_row) == -m:
                        return -1
                        
                # Check columns
                if i <= n - m:
                    score_row = [grid[i+k][j] for k in range(m)]
                    if sum(score_row) == m:
                        return 1
                    elif sum(score_row) == -m:
                        return -1
                        
                # Check diagonal (top-left to bottom-right)
                if i <= n - m and j <= n - m:
                    score_diag_tl_br = [grid[i+k][j+k] for k in range(m)]
                    if sum(score_diag_tl_br) == m:
                        return 1
                    elif sum(score_diag_tl_br) == -m:
                        return -1
                        
                # Check diagonal (bottom-left to top-right)
                if i >= m-1 and j <= n - m:
                    score_diag_bl_tr = [grid[i-k][j+k] for k in range(m)]
                    if sum(score_diag_bl_tr) == m:
                        return 1
                    elif sum(score_diag_bl_tr) == -m:
                        return -1
                    
        return 0
    
    def get_empty_squares(self):
        # print(self.squares)
        return np.argwhere(self.squares == 0)
        
    def is_empty_square(self, row, col):
        return self.squares[row][col] == 0
    
    def is_board_full(self):
        return self.marked_squares == self.size**2
    
    def is_board_empty(self):
        return self.marked_squares == 0
        
    def print_board(self):
        grid = self.squares.copy()
        grid = grid.astype(str)
        grid[grid == '0'] = '-'
        grid[grid == '1'] = 'X'
        grid[grid == '-1'] = 'O'
        
        for row in grid:
            print(row)
            
class Bot:
    """
    Bot class that implements the minimax algorithm.
    Here, the bot is the minimizer and the player is the maximizer.
    """
    def __init__(self, level: int, bot_mark) -> None:
        self.level = level
        self.bot_mark = bot_mark
    
    def random_move(self, board) -> Tuple[int, int]:
        empty_squares = board.get_empty_squares()
        random_square = empty_squares[np.random.randint(len(empty_squares))]
        return random_square
    
    def minimax(self, board, is_maximizing, depth=None, 
                alpha: float=-float('inf'), beta: float=float('inf')):
        # print(f"Board: {board.squares}")
        # terminal states
        opponent = 1 if self.bot_mark == -1 else -1
        
        state = board.check_win()
        
        # bot wins              
        if state == self.bot_mark:
            return -1, None # eval, move
        
        # player wins
        if state == opponent:
            return 1, None # eval, move
        
        # draw 
        if board.is_board_full():
            return 0, None # eval, move
        
        if is_maximizing:
            max_score = -float('inf')
            best_move = None
            
            for row, col in board.get_empty_squares():
                temp_board = copy.deepcopy(board)
                
                temp_board.mark_square(row, col, opponent)
                score, _ = self.minimax(temp_board, False, alpha=alpha, beta=beta)
                
                if score > max_score:
                    max_score = score
                    best_move = (row, col)
                    
                alpha = max(alpha, max_score)
                if alpha >= beta:
                    break
                    
            return max_score, best_move
        
        else:
            min_score = float('inf')
            best_move = None
            
            for row, col in board.get_empty_squares():
                temp_board = copy.deepcopy(board)
                
                temp_board.mark_square(row, col, self.bot_mark)
                score, _ = self.minimax(temp_board, True, alpha=alpha, beta=beta)
                
                if score < min_score:
                    min_score = score
                    best_move = (row, col)
                    
                beta = min(beta, min_score)
                if alpha >= beta:
                    break
            return min_score, best_move
            
        
    
    def eval(self, board):
        if self.level == 0:
            # make a random move
            score = 'random'
            move = self.random_move(board)
        
        else:
            # make a move based on the heuristic and minimax algorithm
            start = time.time()
            score, move = self.minimax(board, False)
            print(f"Bot took {time.time() - start} seconds to make a move")

        print(f"Bot's move: {move} with score {score}")
        
        
        return score, move
    
    
def main():
    
    board = Board(4, 3)
    # grid = board.squares
    board.print_board()
    bot = Bot(1, -1)
    score = None
    
    while True:
        num1, num2 = map(int, input("Enter two space-separated integers: ").split())
        
        if not board.is_empty_square(num1, num2):
            print("Invalid move")
            continue
        
        board.mark_square(num1, num2, 1)
        board.print_board()

        print(">>> Bot's turn: ")
        
        score, next_move = bot.eval(board)
        
        if next_move:
            x, y = next_move
        
            board.mark_square(x, y, -1)
            board.print_board()
            
        else:
            if score == 0:
                print(">>> Game is a draw <<<")
            elif score == 1:
                print(">>> Player wins <<<")
            elif score == -1:
                print(">>> Bot wins <<<")    
            break
if __name__ == '__main__':
    main()
    