class Solution:
    def luckyNumbers(self, matrix: list[list[int]]) -> list[int]:
        lucky_numbers = []
        row_size = len(matrix)
        col_size = len(matrix[0])
        if row_size == 0 or col_size == 0:
            return lucky_numbers

        for i in range(0, row_size):
            min_in_row = min(matrix[i])
            min_in_row_index = matrix[i].index(min_in_row) 

            is_lucky = True
            for j in range(0, row_size):
                if matrix[j][min_in_row_index] > min_in_row:
                    is_lucky = False
                    break

            if is_lucky is True:
                lucky_numbers.append(min_in_row)

        return lucky_numbers