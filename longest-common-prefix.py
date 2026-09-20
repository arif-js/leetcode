from typing import List

class Solution:
    def returnEmpty(self):
        return ""

    def longestCommonPrefix(self, strs: list[str]) -> str:
        lenth_of_array = len(strs)
        length_of_first_str = len(strs[0])
        first_str = strs[0]
        not_matched = False
        matched_prefix = ""

        if lenth_of_array == 1:
            return first_str

        length_of_second_str = len(strs[1])
        lowest_length = length_of_first_str if length_of_first_str < length_of_second_str else length_of_second_str

        for i in range(0, lowest_length):
            if strs[0][i] != strs[1][i]:
                break
            else:
                matched_prefix += strs[1][i]

        if len(matched_prefix) == 0:
            return self.returnEmpty()

        lowest_length = len(matched_prefix)

        for i in range(2, lenth_of_array):
            length_of_new_str = len(strs[i])
            if lowest_length > length_of_new_str:
                lowest_length = length_of_new_str
            matched_prefix = matched_prefix[0:lowest_length]
            for j in range(0, lowest_length):
                if matched_prefix[j] != strs[i][j]:
                    not_matched = True
                    break

            if not_matched == True:
                matched_prefix = matched_prefix[0:j]
                break

        return matched_prefix
