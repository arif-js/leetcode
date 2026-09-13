from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        max_area = 0
        left = 0
        right = len(height) - 1
        max_height = max(height)

        while left < right:
            y = min(height[left], height[right])
            x = right - left
            area = x * y
            if area > max_area:
                max_area = area

            if (height[right] >= max_height and max_area >= area) or (height[left] < height[right]):
                left += 1
            elif height[right] < max_height:
                right -= 1

        return max_area
