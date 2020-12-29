import numpy as np

class SudokuSolution:
    def __init__(self, mat):
        if mat.shape != (9, 9):
            raise Exception("Wrong Size of Sudoku")
        self.mat = mat.copy() % 10
        self.assign = mat.copy() % 10

    def is_complete(self):
        return np.sum(self.assign == 0) == 0

    def select_unassigned_value(self):
        emptys = np.where(self.assign == 0)
        return emptys[0][0], emptys[1][0]

    def detect_avail_values(self, fill_x, fill_y):
        candidates = set(range(1,10))
        y_row = set(self.assign[fill_x].tolist())
        x_row = set(self.assign[:,fill_y].tolist())
        x_blk = int(fill_x/3)
        y_blk = int(fill_y/3)
        block = set(self.assign[x_blk*3:x_blk*3+3,y_blk*3:y_blk*3+3].flatten())
        candidates = candidates-x_row-y_row-block
        return candidates

    def solve(self, debug=False):
        if self.is_complete():
            return self.assign
        fill_x, fill_y = self.select_unassigned_value()
        for x in self.detect_avail_values(fill_x, fill_y):
            self.assign[fill_x][fill_y] = x
            if debug:
                print(self.assign)
                input()
            result = self.solve(debug)
            if result is not None:
                return result
            self.assign[fill_x][fill_y] = 0
        return None

if __name__ == "__main__":
    sudokuGrid = np.array([
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ])
    sol = SudokuSolution(sudokuGrid)
    print(sol.solve())



