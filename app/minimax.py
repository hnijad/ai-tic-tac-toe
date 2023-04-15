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


def minimax(board, cur_depth, depth_limit, is_max, mark, side, alpha, beta):
    score = heuristic(board, 3, side)
    if score is not None:
        return score

    moves = get_possible_moves(board)

    if is_max:
        v = float('-inf')
        for i, j in moves:
            board_copy = get_board_copy(board)
            board_copy[i][j] = mark
            res = minimax(board_copy, cur_depth + 1, depth_limit, False, 'X', side, alpha, beta)
            v = max(v, res)
            alpha = max(alpha, res)
            if beta <= alpha:
                break
        return v

    v = float('inf')
    for i, j in moves:
        board_copy = get_board_copy(board)
        board_copy[i][j] = mark
        res = minimax(board_copy, cur_depth + 1, depth_limit, True, 'O', side, alpha, beta)
        v = min(v, res)
        beta = min(beta, res)
        if beta <= alpha:
            break
    return v


def find_best_move(grid, side):
    moves = get_possible_moves(grid)
    best_score = float('-inf')
    x, y = -1, -1
    for i, j in moves:
        grid[i][j] = side
        score = minimax(grid, 0, 5, False, 'O' if side == 'X' else 'X', side, float('-inf'), float('+inf'))
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
    b = [['-'] * 3 for _ in range(3)]

    while True:
        num1, num2 = map(int, input("Enter two space-separated integers: ").split())
        
        if b[num1][num2] != '-':
            print("Invalid move")
            continue
        
        b[num1][num2] = 'X'
        print_board(b)

        time.sleep(3)

        x, y = find_best_move(b, 'O')
        if x == -1:
            sys.exit(0)
        b[x][y] = 'O'
        print_board(b)


def computer():
    b = [['-'] * 3 for _ in range(3)]

    while True:
        # time.sleep(3)
        x, y = find_best_move(b, 'X')
        if x == -1:
            sys.exit(0)
        b[x][y] = 'X'
        print_board(b)

        time.sleep(3)

        # num1, num2 = map(int, input("Enter two space-separated integers: ").split())
        x, y = find_best_move(b, 'O')

        b[x][y] = 'O'
        print_board(b)


human()
