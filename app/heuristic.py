def heuristic(grid, target, side):
    """
    Calculates the heuristic value for a given game state
    """
    n = len(grid)
    m = target
    
    # Calculate the number of lines of length m that each player has open
    num_lines = {side: 0, -side: 0}
    for i in range(n):
        for j in range(n):
            # Check rows
            if j <= n - m:
                row = [grid[i][j+k] for k in range(m)]
                if abs(sum(row)) == m:
                    num_lines[sum(row)] += 1
                    
            # Check columns
            if i <= n - m:
                col = [grid[i+k][j] for k in range(m)]
                if abs(sum(col)) == m:
                    num_lines[sum(col)] += 1
                    
            # Check diagonal (top-left to bottom-right)
            if i <= n - m and j <= n - m:
                diag_tl_br = [grid[i+k][j+k] for k in range(m)]
                if abs(sum(diag_tl_br)) == m:
                    num_lines[sum(diag_tl_br)] += 1
                    
            # Check diagonal (bottom-left to top-right)
            if i >= m-1 and j <= n - m:
                diag_bl_tr = [grid[i-k][j+k] for k in range(m)]
                if abs(sum(diag_bl_tr)) == m:
                    num_lines[sum(diag_bl_tr)] += 1

    # Calculate the heuristic value based on the number of open lines
    heuristic_value = num_lines[side] - num_lines[-side]

    return heuristic_value
