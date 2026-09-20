import math
from collections import deque
from typing import List

def get_coordinate(square: int, n: int):
    zero_idx = square - 1

    row_from_bottom = zero_idx // n

    r = (n - 1) - row_from_bottom

    c = zero_idx % n

    if row_from_bottom % 2 != 0:
        c = (n - 1) - c

    return r,c

class Solution:
    def snakesAndLadders(self, board: list[list[int]]) -> int:
        n = len(board)
        queue = deque()
        visited = dict()
        processing = dict()

        curr = 1
        count = 0
        queue.append({ "level": count, "value": curr})

        while len(list(queue)) != 0:
            item = queue.popleft()
            curr = item["value"]
            count = item["level"]

            r, c = get_coordinate(curr, n)

            if board[r][c] != -1:
                curr = board[r][c]

            if curr == n*n:
                return count

            for i in range(1,7):
                if curr + i >= curr + 1 and curr + i <= min(curr + 6, n*n):
                    if visited.get(curr + i, 0)!= 1 and processing.get(curr + i, 0) != 1:
                        queue.append({ "level": count + 1, "value": curr + i })
                        processing[curr+i] = 1

            visited[i] = 1

        if len(list(queue)) == 0 and curr != n*n:
            return -1
