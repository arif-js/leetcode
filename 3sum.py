class Solution(object):
    def threeSum(self, nums):
        nums.sort()
        result = list()
        ln = len(nums)
        print(ln)

        hsh = dict()

        for i in range(0, ln-2):
            k = len(nums) - 1
            j = i + 1
            if (nums[i] > 0):
                break
            while j < ln-1 and k > j:
                if nums[i] + nums[j] + nums[k] > 0:
                    k -= 1
                else:
                    if nums[i] + nums[j] + nums[k] == 0:
                        if str(nums[i])+str(nums[k])+str(nums[j]) not in hsh:
                            result.append([nums[i], nums[k], nums[j]])
                            hsh[str(nums[i])+str(nums[k])+str(nums[j])] = 1
                    j+=1

        return result
