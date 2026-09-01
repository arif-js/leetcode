from typing import List

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = list()
        hsh = dict()

        def dfs(curr):
            if len(curr) == len(nums):
                res.append(list(curr))

            for i in range (0, len(nums)):
                if hsh.get(nums[i]) is None:
                    curr.append(nums[i])
                    hsh[nums[i]] = True
                    dfs(curr)
                    curr.pop()
                    hsh.pop(nums[i])

        dfs([])

        return res
