class Solution:
    def intervalIntersection(self, firstList: List[List[int]], secondList: List[List[int]]) -> List[List[int]]:
        firstListLen = len(firstList)
        secondListLen = len(secondList)
        result = []

        if firstListLen == 0 or secondListLen == 0:
            return []

        for i in range(0, firstListLen):
            for j in range(0, secondListLen):
                if firstList[i][0] >= secondList[j][0]:
                    if firstList[i][1] <= secondList[j][1] and firstList[i][0] <= firstList[i][1]:
                        result.append([firstList[i][0],firstList[i][1]])
                    elif firstList[i][1] >= secondList[j][1] and firstList[i][0] <= secondList[j][1]:
                        result.append([firstList[i][0],secondList[j][1]])
                elif firstList[i][0] <= secondList[j][0]:
                    if firstList[i][1] <= secondList[j][1] and secondList[j][0] <= firstList[i][1]:
                        result.append([secondList[j][0],firstList[i][1]])
                    elif firstList[i][1] >= secondList[j][1] and secondList[j][0] <= secondList[j][1]:
                        result.append([secondList[j][0],secondList[j][1]])

        return result
