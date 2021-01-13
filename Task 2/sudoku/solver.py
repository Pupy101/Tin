from itertools import product


def find_unknown(size, table):
    for i in range(size**2):
        for j in range(size**2):
            if table[i][j] == 0:
                return i, j


def set_values(table, size, i, j):
    k, m = i // size, j // size
    set_i_j = list(range(1, 10))
    for _ in range(size**2):
        if table[_][j] != 0 and table[_][j] in set_i_j:
            set_i_j.remove(table[_][j])
        if table[i][_] != 0 and table[i][_] in set_i_j:
            set_i_j.remove(table[i][_])
    for i in range(size):
        for j in range(size):
            if table[k*size+i][m*size+j] != 0 and table[k*size+i][m*size+j] in set_i_j:
                set_i_j.remove(table[k*size+i][m*size+j])
    return set_i_j


def iter_solving_sudoku(size, table):
    solving = []
    index = 0
    replace_previos = False
    d = {}
    while sum(1 for line in table for _ in line if _ != 0) != size**4:
        if not replace_previos:
            i, j = find_unknown(size, table)
            if (i, j) not in d.keys():
                d[(i, j)] = index
                solving.append(((i, j), set_values(table, size, i, j)))
            else:
                solving[d[(i, j)]] = (i, j), set_values(table, size, i, j)
        else:
            try:
                solving[index][1].pop(0)
            except IndexError:
                pass
            replace_previos = False
        if not len(solving[index][1]):
            table[solving[index][0][0]][solving[index][0][1]] = 0
            index -= 1
            replace_previos = True
            continue
        table[solving[index][0][0]][solving[index][0][1]] = solving[index][1][0]
        yield solving[index][0], solving[index][1][0]
        index += 1


def find_solve_sudoku(size, grid):
    R, C = size
    N = R * C
    X = ([("rc", rc) for rc in product(range(N), range(N))] +
         [("rn", rn) for rn in product(range(N), range(1, N + 1))] +
         [("cn", cn) for cn in product(range(N), range(1, N + 1))] +
         [("bn", bn) for bn in product(range(N), range(1, N + 1))])
    Y = dict()
    for r, c, n in product(range(N), range(N), range(1, N + 1)):
        b = (r // R) * R + (c // C)
        Y[(r, c, n)] = [
            ("rc", (r, c)),
            ("rn", (r, n)),
            ("cn", (c, n)),
            ("bn", (b, n))]
    X, Y = exact_cover(X, Y)
    for i, row in enumerate(grid):
        for j, n in enumerate(row):
            if n:
                select(X, Y, (i, j, n))
    for solution in solve(X, Y, []):
        for (r, c, n) in solution:
            grid[r][c] = n
        yield grid


def exact_cover(X, Y):
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X, Y


def solve(X, Y, solution):
    if not X:
        yield list(solution)
    else:
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            solution.append(r)
            cols = select(X, Y, r)
            for s in solve(X, Y, solution):
                yield s
            deselect(X, Y, r, cols)
            solution.pop()


def select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols


def deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)
