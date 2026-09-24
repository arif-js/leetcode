class Solution:
    def angleClock(self, hour: int, minutes: int) -> float:
        hr = 5 * hour # converting to 1-59 range

        div = minutes/60 if minutes != 0 else 0
        hr_change = 5 * div
        new_hr = hr + hr_change

        minutes_distance_1 = abs(new_hr - minutes)
        minutes_distance_2 = 0

        if minutes > new_hr:
            minutes_distance_2 = 60 - minutes + new_hr
        else:
            minutes_distance_2 = minutes + 60 - new_hr

        angle_1 = minutes_distance_1 * 6
        angle_2 = minutes_distance_2 * 6

        return angle_1 if angle_1 < angle_2 else angle_2
