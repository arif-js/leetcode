import math


class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        row_size = len(matrix)
        col_size = len(matrix[0])
        spiral_arr = []

        if len(matrix) == 1:
            return matrix[0]

        curr_row = 0
        curr_col = 0

        visited = dict()
        row_low = 0
        row_high = row_size - 1
        col_low = 0
        col_high = col_size - 1

        for c in range(0, math.ceil(min(row_size, col_size) / 2)):
            for i in range(curr_col, col_high + 1):
                if visited.get(str(curr_row) + str(i), -1) != 1:
                    spiral_arr.append(matrix[curr_row][i])
                    visited[str(curr_row) + str(i)] = 1
                    curr_col = i

            row_low = row_low + 1 if row_low + 1 < row_size else row_low
            curr_row = curr_row + 1 if curr_row + 1 < row_size else curr_row

            for i in range(curr_row, row_high + 1):
                if visited.get(str(i) + str(curr_col), -1) != 1:
                    spiral_arr.append(matrix[i][curr_col])
                    visited[str(i) + str(curr_col)] = 1
                    curr_row = i

            col_high = col_high - 1 if col_high - 1 > -1 else col_high
            curr_col = curr_col - 1 if curr_col - 1 > -1 else curr_col

            for i in range(curr_col, col_low - 1, -1):
                if visited.get(str(curr_row) + str(i), -1) != 1:
                    spiral_arr.append(matrix[curr_row][i])
                    visited[str(curr_row) + str(i)] = 1
                    curr_col = i

            row_high = row_high - 1 if row_high - 1 > -1 else row_high
            curr_row = curr_row - 1 if curr_row - 1 > -1 else curr_row

            for i in range(curr_row, row_low - 1, -1):
                if visited.get(str(i) + str(curr_col), -1) != 1:
                    spiral_arr.append(matrix[i][curr_col])
                    visited[str(i) + str(curr_col)] = 1
                    curr_row = i

            col_low = col_low + 1 if col_low + 1 < col_size else col_low
            curr_col = curr_col + 1 if curr_col + 1 < col_size else curr_col

        return spiral_arr
