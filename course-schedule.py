from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adjacency_list = dict()

        if len(prerequisites) == 0:
            return True
        for course, prereq in prerequisites:
            adjacency_list.setdefault(prereq, []).append(course)

        in_degree = dict()
        for course, prereq in prerequisites:
            if course == prereq:
                return False
            in_degree[course] = in_degree.setdefault(course, 0) + 1
            in_degree[prereq] = in_degree.setdefault(prereq, 0)

        in_degree = dict(sorted(in_degree.items(), key=lambda item: item[1]))
        queue = []
        first_entry = next(iter(in_degree.items())) if len(in_degree.items()) > 0 else None

        if first_entry[1] > 0:
            return False
        queue.append(first_entry[0])

        while len(queue) != 0:
            current_course = queue.pop(0)
            dependent_courses = adjacency_list.get(current_course, [])
            in_degree.pop(current_course)
            for dependent_course in dependent_courses:
                in_degree[dependent_course] = in_degree.get(dependent_course) - 1
                if in_degree[dependent_course] == 0:
                    queue.append(dependent_course)

            if len(queue) == 0 and len(in_degree.keys()) != 0:
                in_degree = dict(sorted(in_degree.items(), key=lambda item: item[1]))
                first_entry = next(iter(in_degree.items())) if len(in_degree.items()) > 0 else None

                if first_entry[1] > 0:
                    return False
                queue.append(first_entry[0])

        return False if len(in_degree.items()) > 0 else True
