class Solution(object):
    def topStudents(self, positive_feedback, negative_feedback, report, student_id, k):
        """
        :type positive_feedback: List[str]
        :type negative_feedback: List[str]
        :type report: List[str]
        :type student_id: List[int]
        :type k: int
        :rtype: List[int]
        """
        hsh = dict()

        for it in range(0, len(positive_feedback)):
            hsh[positive_feedback[it]] = 3

        for it in range(0, len(negative_feedback)):
            hsh[negative_feedback[it]] = -1

        points = dict()

        for it in range(0, len(report)):
            splitted = report[it].split(' ')

            point = 0
            for j in range(0, len(splitted)):
                point += hsh.get(splitted[j], 0)

            points[student_id[it]] = point

        sorted_data = sorted(points.items(), key=lambda x: (-x[1], x[0]))
        return [item[0] for item in sorted_data[:k]]
