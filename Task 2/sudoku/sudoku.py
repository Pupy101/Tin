import random
from sudoku import solver
import pickle


class GenerationSudoku:
    def _generate(self, n, c_k_n):
        self.table = [
            [int((i*n + i/n + j) % (n*n) + 1) for j in range(n*n)]
            for i in range(n*n)]
        GenerationSudoku._mixing(self)
        flook = [
            [0 for j in range(self.size*self.size)]
            for i in range(self.size*self.size)]
        iterator = 0
        difficult = self.size ** 4
        while iterator < self.size ** 4 and difficult > c_k_n:
            i, j = random.randrange(0, self.size*self.size, 1),\
                random.randrange(0, self.size*self.size, 1)
            if flook[i][j] == 0:
                iterator += 1
                flook[i][j] = 1
                temp = self.table[i][j]
                self.table[i][j] = 0
                difficult -= 1
                table_solution = []
                for copy_i in range(0, self.size*self.size):
                    table_solution.append(self.table[copy_i][:])
                i_solution = sum(1 for _ in solver.find_solve_sudoku(
                    (self.size, self.size), table_solution))
                if i_solution != 1:
                    self.table[i][j] = temp
                    difficult += 1

    def _transposing(self):
        self.table = list(map(list, zip(*self.table)))

    def _swap_rows(self):
        area = random.randrange(0, self.size, 1)
        line1 = random.randrange(0, self.size, 1)
        N1 = area*self.size + line1
        line2 = random.randrange(0, self.size, 1)
        while line1 == line2:
            line2 = random.randrange(0, self.size, 1)
        N2 = area*self.size + line2
        self.table[N1], self.table[N2] = self.table[N2], self.table[N1]

    def _swap_colums(self):
        GenerationSudoku._transposing(self)
        GenerationSudoku._swap_rows(self)
        GenerationSudoku._transposing(self)

    def _swap_rows_area(self):
        area1 = random.randrange(0, self.size, 1)
        area2 = random.randrange(0, self.size, 1)
        while area1 == area2:
            area2 = random.randrange(0, self.size, 1)
        for i in range(0, self.size):
            N1, N2 = area1*self.size + i, area2*self.size + i
            self.table[N1], self.table[N2] = self.table[N2], self.table[N1]

    def _swap_colums_small(self):
        GenerationSudoku._transposing(self)
        GenerationSudoku._swap_rows_area(self)
        GenerationSudoku._transposing(self)

    def _mixing(self):
        funcs = [
            'GenerationSudoku._transposing(self)',
            'GenerationSudoku._swap_rows(self)',
            'GenerationSudoku._swap_colums(self)',
            'GenerationSudoku._swap_rows_area(self)',
            'GenerationSudoku._swap_colums_small(self)'
        ]
        for _ in range(random.randint(10, 50)):
            exec(funcs[random.randint(0, 4)])


class Sudoku:
    def __init__(self, *, n=3, count_known_elem=40):
        self.size = n
        self.count_known_elem = count_known_elem
        GenerationSudoku._generate(self, n, count_known_elem)

    def show(self):
        for line in self.table:
            for elem in line:
                print('|'+(str(elem) if elem != 0 else '*').center(4), end='')
            print('|')

    def _check(self, index):
        return 0 <= index < self.size*2

    def input_number(self, row, col, value, comp=False):
        if ((self.table[row][col] != 0
        or (not self._check(row) and not self._check(col)))
        and not comp):
            raise ValueError
        self.table[row][col] = value

    def save_game(self, path):
        with open(path+'.pkl', 'wb') as f:
            pickle.dump(self, f)

    def end(self):
        s = sum(1 for i in range(self.size**2)
        for j in range(self.size**2) if self.table[i][j] != 0)
        return s == self.size ** 4
