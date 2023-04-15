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


def heuristic2(grid, target, side, turn):
    rows = len(grid)
    cols = len(grid[0])

    max_x = -1
    max_o = -1

    cnt_x = 0
    cnt_o = 0

    for k in range(target, 0, -1):  # optimize
        for i in range(rows - k + 1):
            for j in range(cols - k + 1):
                #print(k)
                if k == target:
                    if all(grid[i + d][j + d] in ('X', '-') for d in range(k)):
                        cnt_x += 1
                        #print("possible,", i, j, k)

                if all(grid[i + d][j + d] in 'X' for d in range(k)):
                    max_x = max(max_x, k)

                if k == target:
                    if all(grid[i + d][j + d] in ('O', '-') for d in range(k)):
                        cnt_o += 1

                if all(grid[i + d][j + d] in 'O' for d in range(k)):
                    max_o = max(max_o, k)

                if k == target:
                    if all(grid[i + d][j + k - d - 1] in ('X', '-') for d in range(k)):
                        cnt_x += 1

                if all(grid[i + d][j + k - d - 1] in 'X' for d in range(k)):
                    max_x = max(max_x, k)

                if k == target:
                    if all(grid[i + d][j + k - d - 1] in ('O', '-') for d in range(k)):
                        cnt_o += 1

                if all(grid[i + d][j + k - d - 1] in 'O' for d in range(k)):
                    max_o = max(max_o, k)

    for k in range(target, 0, -1):
        for i in range(rows):
            for j in range(cols - k + 1):
                if k == target:
                    if all(grid[i][j + d] in ('X', '-') for d in range(k)):
                        cnt_x += 1

                if all(grid[i][j + d] in 'X' for d in range(k)):
                    max_x = max(max_x, k)

                if k == target:
                    if all(grid[i][j + d] in ('O', '-') for d in range(k)):
                        cnt_o += 1

                if all(grid[i][j + d] in 'O' for d in range(k)):
                    max_o = max(max_o, k)

    for k in range(target, 0, -1):
        for i in range(rows - k + 1):
            for j in range(cols):
                if k == target:
                    if all(grid[i + d][j] in ('X', '-') for d in range(k)):
                        cnt_x += 1
                        #print("possible,", i, k)

                if all(grid[i + d][j] in 'X' for d in range(k)):
                    max_x = max(max_x, k)

                if k == target:
                    if all(grid[i + d][j] in ('O', '-') for d in range(k)):
                        cnt_o += 1
                        #print("possible,", i, j, k)

                if all(grid[i + d][j] in 'O' for d in range(k)):
                    max_o = max(max_o, k)

    if not any('-' in row for row in grid):
        return 0

    #print("cnt ", cnt_o, cnt_x)
    #print("max ", max_x, max_o)

    if cnt_o == 0 and cnt_x == 0:
        return 0
    if side == 'X':
        # if cnt_o >= cnt_x:
        #     return -1
        # return 1
        #return (cnt_x - cnt_o) + (max_x -max_o)
        return target - max_o
    # if cnt_x >= cnt_o:
    #     return -1
    # return 1
    #return (cnt_o - cnt_x) + (max_o - max_x)
    if max_x == target:
        return -10
    return target - max_x


cache = {}


def minimax(board, cur_depth, depth_limit, is_max, mark, side, alpha, beta, target):
    score = heuristic2(board, target, side, 'X' if is_max == True else 'O')

    key = tuple(tuple(row) for row in board)

    if key in cache:
        return cache[key]

    if cur_depth >= depth_limit:
        return score

    moves = get_possible_moves(board)

    if is_max:
        v = float('-inf')
        for i, j in moves:
            board_copy = get_board_copy(board)
            board_copy[i][j] = mark
            res = minimax(board_copy, cur_depth + 1, depth_limit, False, 'X', side, alpha, beta, target)
            v = max(v, res)
            alpha = max(alpha, res)
            if beta <= alpha:
                break
        cache[key] = v
        return v

    v = float('inf')
    for i, j in moves:
        board_copy = get_board_copy(board)
        board_copy[i][j] = mark
        res = minimax(board_copy, cur_depth + 1, depth_limit, True, 'O', side, alpha, beta, target)
        v = min(v, res)
        beta = min(beta, res)
        if beta <= alpha:
            break
    cache[key] = v
    return v


def find_best_move(grid, side, target):
    moves = get_possible_moves(grid)
    best_score = float('-inf')
    depth = min(target // 2 + 1, 5)
    x, y = -1, -1
    for i, j in moves:
        grid[i][j] = side
        score = minimax(grid, 0, depth, False, 'O' if side == 'X' else 'X', side, float('-inf'), float('+inf'), target)
        grid[i][j] = '-'
        # print("i, j", i, j, score)
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
        b[num1][num2] = 'X'
        print_board(b)

        time.sleep(3)

        x, y = find_best_move(b, 'O', target)
        if x == -1:
            sys.exit(0)
        b[x][y] = 'O'
        print_board(b)


def computer():
    b = [['-'] * 3 for _ in range(3)]

    while True:
        time.sleep(3)
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

# b = [['X', 'O', 'O', '-', '-', '-'],
#      ['X', '-', 'X', 'X', 'O', 'O'],
#      ['-', '-', 'O', 'X', '-', '-'],
#      ['-', 'O', 'X', 'X', '-', '-'],
#      ['O', '-', '-', 'O', '-', '-'],
#      ['X', 'O', '-', '-', '-', 'X']]

#print(heuristic2(b, 5, 'O', 'X'))

#b = [['-'] * 6 for _ in range(6)]
#print(heuristic2(b, 6, 'X', 'X'))
# b[3][3] = 'X'
# b[0][0] = 'O'
# print_board(b)
# print(heuristic2(b, 6, 'O', 'X'))

#
# b[1][1] = b[2][2] = b[3][3] = 'X'
#
# b[2][0] = b[3][0] = b[4][0] = 'O'
#
# print_board(b)
# print(heuristic2(b, 6, 'X'))


