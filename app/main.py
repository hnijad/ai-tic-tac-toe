import time
import sys
from client.GameServerClient import GameServerClient
from config import get_input_config


def count_moves(grid):
    count = 0
    for row in grid:
        for char in row:
            if char != '-':
                count += 1
    return count


def find_move(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '-':
                return i, j

    return -1, -1


def print_board(grid):
    for row in grid:
        print(row, end='\n')


def sync_board(grid, server_board_string):
    rows = server_board_string.strip().split('\n')
    server_board = [[c for c in row] for row in rows]
    change = False
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != server_board[i][j]:
                change = True
                grid[i][j] = server_board[i][j]

    return change


if __name__ == '__main__':
    gsc = GameServerClient()

    board_size = get_input_config('board_size')
    board = [['-'] * board_size for _ in range(board_size)]
    turn = get_input_config('turn')
    team_id = get_input_config('team_id')
    game_id = get_input_config('game_id')

    change_cnt = 0

    while True:
        cnt = count_moves(board)
        if cnt % 2 == (turn + 1) % 2:
            print("My turn: making a move ..")
            x, y = find_move(board)
            if x == -1:
                print("Game is finished!")
                sys.exit(0)
            resp = gsc.make_move(team_id=team_id, game_id=game_id, x=x, y=y)
            if resp['code'] == 'OK':
                board[x][y] = 'O' if turn == 1 else 'X'
                print("Made the move")
            elif 'Game is no longer open' in resp['message']:
                print("Game is no longer open. Exiting ...")
                sys.exit(0)
            else:
                print("Failed to make a move")

        else:
            if change_cnt > 5:
                print("Looks like opponent failed to make a move or the game is finished. Exiting ...")
                sys.exit(0)
            print("Opponent's turn: waiting for a move ...")
            if sync_board(board, gsc.get_board(game_id=game_id)):
                print("Synced the board")
                print_board(board)
                change_cnt = 0
            else:
                change_cnt += 1

            time.sleep(7)
