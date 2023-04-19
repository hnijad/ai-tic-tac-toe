class Board:
    def __init__(self, size, target, turn):
        self.size = size
        self.target = target
        self.turn = turn
        self.state = [['-'] * size for _ in range(size)]

    def is_game_finished(self) -> bool:
        for i in range(self.size - self.target + 1):
            for j in range(self.size - self.target + 1):
                if all(self.state[i + d][j + d] == 'X' for d in range(self.target)):
                    return True

                if all(self.state[i + d][j + d] == 'O' for d in range(self.target)):
                    return True

                if all(self.state[i + d][j + self.target - d - 1] == 'X' for d in range(self.target)):
                    return True

                if all(self.state[i + d][j + self.target - d - 1] == 'O' for d in range(self.target)):
                    return True

        for i in range(self.size):
            for j in range(self.size - self.target + 1):
                if all(self.state[i][j + d] == 'X' for d in range(self.target)):
                    return True

                if all(self.state[i][j + d] == 'O' for d in range(self.target)):
                    return True

        for i in range(self.size - self.target + 1):
            for j in range(self.size):
                if all(self.state[i + d][j] == 'X' for d in range(self.target)):
                    return True

                if all(self.state[i + d][j] == 'O' for d in range(self.target)):
                    return True

        if not any('-' in row for row in self.state):
            return True
        return False

    def make_move(self, x, y, mark):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.state[x][y] = mark
        else:
            raise IndexError("Given indices are out of range. size = {}".format(self.size))

    def reset_move(self, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            self.state[x][y] = '-'
        else:
            raise IndexError("Given indices are out of range. size = {}".format(self.size))

    def __str__(self) -> str:
        board_str = ""
        for row in self.state:
            board_str += "|".join(row) + "\n"
        return board_str

    def evaluate(self):
        max_x, max_o = -1, -1
        cnt_x, cnt_o = 0, 0

        for k in range(self.target, 0, -1):  # optimize
            for i in range(self.size - k + 1):
                for j in range(self.size - k + 1):
                    if k == self.target:
                        if all(self.state[i + d][j + d] in ('X', '-') for d in range(k)):
                            cnt_x += 1

                    if all(self.state[i + d][j + d] in 'X' for d in range(k)):
                        max_x = max(max_x, k)

                    if k == self.target:
                        if all(self.state[i + d][j + d] in ('O', '-') for d in range(k)):
                            cnt_o += 1

                    if all(self.state[i + d][j + d] in 'O' for d in range(k)):
                        max_o = max(max_o, k)

                    if k == self.target:
                        if all(self.state[i + d][j + k - d - 1] in ('X', '-') for d in range(k)):
                            cnt_x += 1

                    if all(self.state[i + d][j + k - d - 1] in 'X' for d in range(k)):
                        max_x = max(max_x, k)

                    if k == self.target:
                        if all(self.state[i + d][j + k - d - 1] in ('O', '-') for d in range(k)):
                            cnt_o += 1

                    if all(self.state[i + d][j + k - d - 1] in 'O' for d in range(k)):
                        max_o = max(max_o, k)

        for k in range(self.target, 0, -1):
            for i in range(self.size):
                for j in range(self.size - k + 1):
                    if k == self.target:
                        if all(self.state[i][j + d] in ('X', '-') for d in range(k)):
                            cnt_x += 1

                    if all(self.state[i][j + d] in 'X' for d in range(k)):
                        max_x = max(max_x, k)

                    if k == self.target:
                        if all(self.state[i][j + d] in ('O', '-') for d in range(k)):
                            cnt_o += 1

                    if all(self.state[i][j + d] in 'O' for d in range(k)):
                        max_o = max(max_o, k)

        for k in range(self.target, 0, -1):
            for i in range(self.size - k + 1):
                for j in range(self.size):
                    if k == self.target:
                        if all(self.state[i + d][j] in ('X', '-') for d in range(k)):
                            cnt_x += 1

                    if all(self.state[i + d][j] in 'X' for d in range(k)):
                        max_x = max(max_x, k)

                    if k == self.target:
                        if all(self.state[i + d][j] in ('O', '-') for d in range(k)):
                            cnt_o += 1

                    if all(self.state[i + d][j] in 'O' for d in range(k)):
                        max_o = max(max_o, k)

        if not any('-' in row for row in self.state):
            return 0

        if cnt_o == 0 and cnt_x == 0:
            return 0

        score = 2 * (cnt_x - cnt_o) + 10 * (max_x - max_o)
        return score if self.get_mark() == 'X' else -score

    def get_possible_moves(self):
        moves = []
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] == '-':
                    moves.append((i, j))
        return moves

    def get_key(self):
        return tuple(tuple(row) for row in self.state)

    def get_mark(self):
        return 'X' if self.turn == 2 else 'O'

    def get_opponent_mark(self):
        return 'O' if self.turn == 2 else 'X'

    def get_depth(self):
        if self.size <= 3:
            return 9
        if self.size <= 5:
            return 3
        if self.size <= 6:
            return 3
        return 1

    def sync_state(self, server_board_string):
        rows = server_board_string.strip().split('\n')
        server_board = [[c for c in row] for row in rows]
        change = False
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] != server_board[i][j]:
                    change = True
                    self.state[i][j] = server_board[i][j]

        return change

    def count_moves(self):
        count = 0
        for row in self.state:
            for char in row:
                if char != '-':
                    count += 1
        return count
