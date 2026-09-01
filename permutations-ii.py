class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        res = list()
        hsh = dict()
        permutation_hsh = dict()

        def dfs(curr):
            if len(curr) == len(nums) and permutation_hsh.get(str(curr)) is None:
                res.append(list(curr))
                permutation_hsh[str(curr)] = True

            for i in range (0, len(nums)):
                if hsh.get(i) is None:
                    curr.append(nums[i])
                    hsh[i] = True
                    dfs(curr)
                    curr.pop()
                    hsh.pop(i)

        dfs([])
        return res
