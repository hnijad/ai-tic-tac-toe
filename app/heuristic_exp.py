def heuristic(grid, target, side):
    score = 0
    opponent = 'O' if side == 'X' else 'X'
    empty_cells = 0
    for i in range(len(grid)):
        row_score = 0
        col_score = 0
        row_opponent = 0
        col_opponent = 0
        for j in range(len(grid[i])):
            if grid[i][j] == side:
                row_score += 1
            elif grid[i][j] == opponent:
                row_opponent += 1
            else:
                empty_cells += 1
            if grid[j][i] == side:
                col_score += 1
            elif grid[j][i] == opponent:
                col_opponent += 1
        if row_score == target:
            return float('inf')
        if row_opponent == target:
            return float('-inf')
        score += row_score - row_opponent
        if col_score == target:
            return float('inf')
        if col_opponent == target:
            return float('-inf')
        score += col_score - col_opponent
    diag_score = 0
    diag_opponent = 0
    for i in range(len(grid)):
        if grid[i][i] == side:
            diag_score += 1
        elif grid[i][i] == opponent:
            diag_opponent += 1
    if diag_score == target:
        return float('inf')
    if diag_opponent == target:
        return float('-inf')
    score += diag_score - diag_opponent
    diag_score = 0
    diag_opponent = 0
    for i in range(len(grid)):
        if grid[i][len(grid)-i-1] == side:
            diag_score += 1
        elif grid[i][len(grid)-i-1] == opponent:
            diag_opponent += 1
    if diag_score == target:
        return float('inf')
    if diag_opponent == target:
        return float('-inf')
    score += diag_score - diag_opponent
    score += empty_cells - (len(grid)**2 - empty_cells)
    return score

