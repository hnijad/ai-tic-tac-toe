import copy
import time
import numpy as np
from typing import List, Tuple

class Board:
    def __init__(self, size, target) -> None:
        self.size = size
        self.target = target
        self.squares = np.array([['-' for _ in range(size)] for _ in range(size)])
        self.empty_squares = self.squares
        self.marked_squares = 0
        
    def mark_square(self, row, col, player_mark):
        self.squares[row][col] = player_mark
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
    """
    Bot class that implements the minimax algorithm.
    Here, the bot is the minimizer and the player is the maximizer.
    """
    def __init__(self, level: int=1, bot_mark: str='O') -> None:
        self.level = level
        self.bot_mark = bot_mark
    
    def random_move(self, board) -> Tuple[int, int]:
        empty_squares = board.get_empty_squares()
        random_square = empty_squares[np.random.randint(len(empty_squares))]
        return random_square
    
    def minimax(self, board, is_maximizing, depth=None):
        # terminal states
        opponent = 'X' if self.bot_mark == 'O' else 'O'
        
        # bot wins              
        if board.check_win(self.bot_mark):
            return -1, None # eval, move
        
        # player wins
        if board.check_win(opponent):
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
                score, _ = self.minimax(temp_board, False)
                
                if score > max_score:
                    max_score = score
                    best_move = (row, col)
                    
            return max_score, best_move
        
        else:
            min_score = float('inf')
            best_move = None
            
            for row, col in board.get_empty_squares():
                temp_board = copy.deepcopy(board)
                
                temp_board.mark_square(row, col, self.bot_mark)
                score, _ = self.minimax(temp_board, True)
                
                if score < min_score:
                    min_score = score
                    best_move = (row, col)
                    
            return min_score, best_move
            
        
    
    def eval(self, board):
        if self.level == 0:
            # make a random move
            score = 'random'
            move = self.random_move(board)
        
        else:
            # make a move based on the heuristic and minimax algorithm
            start = time.time()
            score, move = self.minimax(board, 0, True)
            print(f"Bot took {time.time() - start} seconds to make a move")

        print(f"Bot's move: {move} with score {score}")
        
        
        return score, move
    
    
def main():
    
    board = Board(5, 3)
    # grid = board.squares
    board.print_board()
    bot = Bot(1, 'O')
    
    while True:
        num1, num2 = map(int, input("Enter two space-separated integers: ").split())
        
        if not board.is_empty_square(num1, num2):
            print("Invalid move")
            continue
        
        board.mark_square(num1, num2, 'X')
        board.print_board()

        print(">>> Bot's turn: ")
        
        score, next_move = bot.eval(board)
        
        if next_move:
            x, y = next_move
        
            board.mark_square(x, y, 'O')
            board.print_board()
        else:
            if score == 0:
                print(">>> Game is a draw <<<")
            elif score == 1:
                print(">>> Player wins <<<")
            elif score == -1:
                print(">>> Bot wins <<<")    
if __name__ == '__main__':
    main()
    