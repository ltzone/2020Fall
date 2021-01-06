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
        if self.is_invalid():
            return None
        return self.rec_solve(debug)

    def rec_solve(self, debug=False):
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

    def is_invalid(self):
        for x in range(9):
            row = set(self.mat[x].tolist())
            if sum(row) != np.sum(self.mat[x]):
                return True
        for y in range(9):
            col = set(self.mat[:,y].tolist())
            if sum(col) != np.sum(self.mat[:,y]):
                return True
        for x_blk in range(3):
            for y_blk in range(3):
                blk = self.mat[x_blk * 3:x_blk * 3 + 3, y_blk * 3:y_blk * 3 + 3]
                if sum(set(blk.flatten())) != np.sum(blk):
                    return True
        return False


if __name__ == "__main__":
    sudokuGrid = np.array(
        [[ 0,  0,  0, 13,  0, 16,  0,  0, 15],
 [ 0,  0, 15, 17,  0, 14,  0,  0, 13],
 [ 0, 17, 11,  0, 12,  0,  0,  0,  0],
 [19, 18,  0,  0,  0, 13,  0,  0,  0],
 [ 0,  0,  0, 16,  0, 18,  0,  0,  0],
 [ 0,  0,  0, 19,  0,  0,  0, 16, 12],
 [ 0,  0,  0,  0,  0,  0, 15, 13,  0],
 [12,  0,  0, 14,  0, 17, 19,  0,  0],
 [13,  0, 14, 15,  0, 19, 12,  0,  0]])
    sol = SudokuSolution(sudokuGrid)
    print(sol.solve())



