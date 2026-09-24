class Solution:
    def angleClock(self, hour: int, minutes: int) -> float:
        hr = 5 * (hour + (minutes/60 if minutes != 0 else 0))

        angle_1 = abs(hr - minutes) * 6
        angle_2 = (60 - minutes + hr if minutes > hr else minutes + 60 - hr) * 6

        return angle_1 if angle_1 < angle_2 else angle_2
