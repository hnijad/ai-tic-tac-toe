import random
import sys

n = 5
a = []
t = 2
team = "X"

for i in range(n):
    a.append([])
    for j in range(n):
        a[i].append('-')
        

a[0][0] = "X"
a[1][1] = "X"
a[2][2] = "O"
a[3][3] = "X"
a[4][4] = "O"
def target(a, t):
    for i in range(n):
        c = 1
        for j in range(1, n):
            if a[i][j] == '-' or a[i][j] != a[i][j-1]:
                c = 0
            else: 
                c+=1
            if c >= t-1:
                return True
    for i in range(n):
        c = 1
        for j in range(1, n):
            if a[j][i] == '-' or a[j][i] != a[j-1][i]:
                c = 0
            else: 
                c+=1
            if c >= t-1:
                return True    
    c = 0
    for i in range(n-1):
        if a[i][i] == a[i+1][i+1]:
            c +=1
        else:
            c =0
        if c >= t-1:
            return True    
        print(a[i][i])
    return False
        
print(target(a, t))

def generate(a, moving):
    successors = []
    for i in range(n):
        for j in range(n):
            if a[i][j] == '-':
                a[i][j] = moving
                successors.append(a[i][j])
    return successors
        
    
def terminate(a, t):
    if target(a, t) or '-' not in sum(a, []):
        return True
    else: return False

def value(a, t, moving):
    if terminate(a, t): return h(a)
    if moving == team:
        return maxf(a)
    else:
        return minf(a)





def h(a):
    return random.randint(1, 100)
    
def maxf(a, moving):
    max_value = -sys.maxsize
    successors = generate(a, moving)
    for successor in successors:
        if max_value < value(successor, t, moving):
            max_value = value(successor, t, moving)
    return max_value

def minf(a, moving):
    min_value = sys.maxsize
    successors = generate(a, moving)
    for successor in successors:
        if min_value > value(successor, t, moving):
            min_value = value(successor, t, moving)
    return min_value


    
    