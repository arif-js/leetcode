from typing import List

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []
        c_ln = len(candidates)
        candidates.sort()

        def findCombinationSum(si, curr, curr_sum):
            if curr_sum == target:
                res.append(list(curr))
                return

            for i in range(si, c_ln):
                if curr_sum + candidates[i] <= target:
                    curr.append(candidates[i])
                    curr_sum += candidates[i]
                    findCombinationSum(i, curr, curr_sum)
                    curr.pop()
                    curr_sum -= candidates[i]
                else:
                    break

        findCombinationSum(0, [], 0)
        return res
