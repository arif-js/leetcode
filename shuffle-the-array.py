from typing import List

class Solution:
    def shuffle(self, nums: List[int], n: int) -> List[int]:
        result = []
        i = 0
        while i < n:
            result.append(nums[i])
            j = i + n
            result.append(nums[j])
            i+=1

        return result
