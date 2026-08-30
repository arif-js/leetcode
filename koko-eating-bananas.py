import math
from typing import List

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        n = len(piles)
        sorted_piles = sorted(piles)
        max_number = sorted_piles[n-1]
        min_number = 1

        l = 1
        r = max_number
        result = 0
        m = math.floor((l+r)/2)
        last_best_m = 0

        while True:
            sum_hours = 0

            for i in range(0, n):
                sum_hours += math.ceil(sorted_piles[i]/m)

            if sum_hours == h:
                last_best_m = m
                r = m - 1
            elif sum_hours < h:
                r = m - 1
                last_best_m = m if m < last_best_m or last_best_m == 0 else last_best_m
            else:
                l = m + 1

            m = math.floor((l+r)/2)

            if r < l or l > m:
                result = last_best_m
                break

        return result
