import sys
import time
from model.board import Board


def minimax(board: Board, cur_depth, depth_limit, is_max, mark, alpha, beta):
    if cur_depth >= depth_limit or board.is_game_finished():
        return board.evaluate()
    moves = board.get_possible_moves()
    if is_max:
        v = float('-inf')
        for i, j in moves:
            board.make_move(i, j, mark)
            res = minimax(board, cur_depth + 1, depth_limit, not is_max, board.get_opponent_mark(), alpha, beta)
            board.reset_move(i, j)
            v = max(v, res)
            alpha = max(alpha, res)
            if beta <= alpha:
                break
        return v

    v = float('inf')
    for i, j in moves:
        board.make_move(i, j, mark)
        res = minimax(board, cur_depth + 1, depth_limit, not is_max, board.get_mark(), alpha, beta)
        board.reset_move(i, j)
        v = min(v, res)
        beta = min(beta, res)
        if beta <= alpha:
            break
    return v


def find_best_move(board: Board, side):
    moves = board.get_possible_moves()
    best_score = float('-inf')
    depth = board.get_depth()
    x, y = -1, -1
    for i, j in moves:
        board.make_move(i, j, side)
        score = minimax(board, 0, depth, False, board.get_opponent_mark(), float('-inf'), float('+inf'))
        board.reset_move(i, j)
        if score > best_score:
            best_score = score
            x, y = i, j
    return x, y


def human():
    board_size, target = map(int, input("Enter board_size and target: ").split())

    board = Board(board_size, target, 2)

    while not board.is_game_finished():
        num1, num2 = map(int, input("Enter two space-separated integers: ").split())
        board.make_move(num1, num2, 'X')

        print(board)
        # time.sleep(3)

        start_time = time.time()
        x, y = find_best_move(board, 'O')
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.6f} seconds")
        if x == -1:
            sys.exit(0)
        board.make_move(x, y, 'O')
        print(board)


def computer():
    pass
    # b = [['-'] * 3 for _ in range(3)]
    #
    # while True:
    #     time.sleep(3)
    #     x, y = find_best_move(b, 'X')
    #     if x == -1:
    #         sys.exit(0)
    #     b[x][y] = 'X'
    #     print_board(b)
    #
    #     time.sleep(3)
    #
    #     # num1, num2 = map(int, input("Enter two space-separated integers: ").split())
    #     x, y = find_best_move(b, 'O')
    #
    #     b[x][y] = 'O'
    #     print_board(b)


