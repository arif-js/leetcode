class Solution(object):
    def canCompleteCircuit(self, gas, cost):
        """
        :type gas: List[int]
        :type cost: List[int]
        :rtype: int
        """
        ln = len(gas)
        traverse_index = 0
        i = 0
        j = 0
        total_gas_now = 0
        while traverse_index < ln:
            total_gas_now = gas[i] + total_gas_now
            if total_gas_now >= cost[i]:
                total_gas_now = total_gas_now - cost[i]
                traverse_index += 1
                i = 0 if i + 1 == ln else i + 1
            elif traverse_index < ln:
                if j + 1 == ln or i + 1 == ln or j > i:
                    break
                j += 1
                i += 1
                j = max(j, i) if i > j else j
                i = j
                traverse_index = 0
                total_gas_now = 0

        result = j if traverse_index == ln else -1
        return result
