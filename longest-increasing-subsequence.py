class Solution(object):
    def lengthOfLIS(self, nums):
        max_ln = 1
        dp = [1] * len(nums)

        for i in range(1, len(nums)):
            max_sum = 1
            for j in range (0, i):
                if nums[i] > nums[j]:
                    max_sum = max(dp[j]+1, max_sum)
            dp[i] = max_sum
            max_ln = max(max_ln, dp[i])

        return max_ln
