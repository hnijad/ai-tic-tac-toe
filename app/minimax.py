import sys
import time


def get_possible_moves(grid):
    moves = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '-':
                moves.append((i, j))
    return moves


def get_board_copy(grid):
    return [row[:] for row in grid]


def heuristic(grid, target, side):
    rows = len(grid)
    cols = len(grid[0])

    for i in range(rows - target + 1):
        for j in range(cols - target + 1):
            if all(grid[i + d][j + d] == 'X' for d in range(target)):
                return 1 if side == 'X' else -1

            if all(grid[i + d][j + d] == 'O' for d in range(target)):
                return -1 if side == 'X' else 1

            if all(grid[i + d][j + target - d - 1] == 'X' for d in range(target)):
                return 1 if side == 'X' else -1

            if all(grid[i + d][j + target - d - 1] == 'O' for d in range(target)):
                return -1 if side == 'X' else 1

    for i in range(rows):
        for j in range(cols - target + 1):
            if all(grid[i][j + d] == 'X' for d in range(target)):
                return 1 if side == 'X' else -1

            if all(grid[i][j + d] == 'O' for d in range(target)):
                return -1 if side == 'X' else 1

    for i in range(rows - target + 1):
        for j in range(cols):
            if all(grid[i + d][j] == 'X' for d in range(target)):
                return 1 if side == 'X' else -1

            if all(grid[i + d][j] == 'O' for d in range(target)):
                return -1 if side == 'X' else 1

    if not any('-' in row for row in grid):
        return 0

    return None

def heuristic_meh(grid, target, side):
    n = len(grid)
    m = target
    opponent = 'O' if side == 'X' else 'X'
    # Calculate the number of lines of length m that each player has open
    num_lines = {side: 0, opponent: 0}
    
    for i in range(n):
        for j in range(n):
            # Check rows
            if j <= n - m:
                side_score_row = [grid[i][j+k] == side for k in range(m)]
                if sum(side_score_row) == m:
                    return 10
                
                opponent_score_row = [grid[i][j+k] == opponent for k in range(m)]
                if sum(opponent_score_row) == m:
                    return -10
                    
            # Check columns
            if i <= n - m:
                side_score_col = [grid[i+k][j] == side for k in range(m)]
                if sum(side_score_col) == m:
                    return 10
                
                opponent_score_col = [grid[i+k][j] == opponent for k in range(m)]
                if sum(opponent_score_col) == m:
                    return -10
                    
            # Check diagonal (top-left to bottom-right)
            if i <= n - m and j <= n - m:
                side_score_diag_tl_br = [grid[i+k][j+k] == side for k in range(m)]
                if sum(side_score_diag_tl_br) == m:
                    return 10
                
                opponent_score_diag_tl_br = [grid[i+k][j+k] == opponent for k in range(m)]
                if sum(opponent_score_diag_tl_br) == m:
                    return -10
                    
            # Check diagonal (bottom-left to top-right)
            if i >= m-1 and j <= n - m:
                side_score_diag_bl_tr = [grid[i-k][j+k] == side for k in range(m)]
                if sum(side_score_diag_bl_tr) == m:
                    return 10
                
                opponent_score_diag_bl_tr = [grid[i-k][j+k] == opponent for k in range(m)]
                if sum(opponent_score_diag_bl_tr) == m:
                    return -10

    # Calculate the heuristic value based on the number of open lines

    return 0

def minimax(board, target, cur_depth, depth_limit, is_max, mark, side, alpha, beta):
    score = heuristic(board, target, side)
    if score is not None:
        return score

    moves = get_possible_moves(board)

    if is_max:
        v = float('-inf')
        for i, j in moves:
            board_copy = get_board_copy(board)
            board_copy[i][j] = mark
            res = minimax(board_copy, target, cur_depth + 1, depth_limit, False, 'X', side, alpha, beta)
            v = max(v, res)
            alpha = max(alpha, res)
            if beta <= alpha:
                break
        return v

    v = float('inf')
    for i, j in moves:
        board_copy = get_board_copy(board)
        board_copy[i][j] = mark
        res = minimax(board_copy, target, cur_depth + 1, depth_limit, True, 'O', side, alpha, beta)
        v = min(v, res)
        beta = min(beta, res)
        if beta <= alpha:
            break
    return v



def find_best_move(grid, target, side):
    moves = get_possible_moves(grid)
    best_score = float('-inf')
    x, y = -1, -1
    for i, j in moves:
        grid[i][j] = side
        score = minimax(grid, target, 0, 5, False, 'O' if side == 'X' else 'X', side, float('-inf'), float('+inf'))
        grid[i][j] = '-'
        if score > best_score:
            best_score = score
            x, y = i, j
    print("log: " + "side=" + side + ", bs=" + str(best_score) + ", pos=" + str(x) + "," + str(y), end="\n")
    return x, y


def is_finished(grid):
    pass


def print_board(grid):
    for row in grid:
        print(row, end='\n')


def human():
    
    board_size, target = map(int, input("Enter board_size and target: ").split())

    b = [['-'] * board_size for _ in range(board_size)]

    while True:
        num1, num2 = map(int, input("Enter two space-separated integers: ").split())
        
        if b[num1][num2] != '-':
            print("Invalid move")
            continue
        
        b[num1][num2] = 'X'
        print_board(b)

        # time.sleep(3)

        x, y = find_best_move(b, target, 'O')
        if x == -1:
            sys.exit(0)
        b[x][y] = 'O'
        print_board(b)


human()
