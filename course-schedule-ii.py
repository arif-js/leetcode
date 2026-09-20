from collections import defaultdict, deque

class Solution:
    def findOrder(self, numCourses: int, prerequisites: list[list[int]]) -> list[int]:
        adj = defaultdict(list)
        inbound_count = defaultdict(list)
        result = []
        visited = defaultdict(bool)

        if len(prerequisites) == 0:
            for i in range(0, numCourses):
                result.append(i)
        else:
            for i in range(0, numCourses):
                inbound_count[i] = 0
                visited[i] = False

            for a, b in prerequisites:
                adj[b].append(a)  # b -> a
                inbound_count[a] = inbound_count.get(a, 0) + 1

            inbound_count = dict(sorted(inbound_count.items(), key=lambda x: x[1]))

            queue = deque()
            first_item = next(iter(inbound_count))
            queue.append(first_item)

            if inbound_count[first_item] != 0:
                return []

            del inbound_count[first_item]

            while len(queue) != 0:
                picked = queue.popleft()
                result.append(picked)

                for each_adj in adj[picked]:
                    inbound_count[each_adj] = inbound_count.get(each_adj, 0) - 1

                    if inbound_count[each_adj] == 0 and visited[each_adj] != True:
                        del inbound_count[each_adj]
                        queue.append(each_adj)
                        visited[each_adj] = True

                if len(queue) == 0 and len(inbound_count) > 0 and inbound_count.get(next(iter(inbound_count)), 0) == 0:
                    next_item = next(iter(inbound_count))
                    queue.append(next_item)
                    del inbound_count[next_item]


        if len(result) != numCourses:
            return []
        return result
