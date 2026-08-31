class Solution:
    def calculate(self, s: str) -> int:
        s = s.replace(' ', '')
        s = s+"s"
        stack = []
        ln = len(s)
        i = 0
        j = 0
        last_char = ''

        while i < ln:
            if s[i] == '+' or s[i] == '-' or s[i] == '*' or s[i] == '/' or s[i] == 's':
                if last_char == '/' or last_char == '*':
                    stack.pop()
                    popped_item = int(stack.pop())
                    result = popped_item * int(s[j:i]) if last_char == '*' else  popped_item / int(s[j:i])
                    stack.append(result)
                else:
                    stack.append(s[j:i])

                if s[i] != 's':
                    stack.append(s[i])
                    last_char = s[i]
                    j += len(s[j:i])+1

            i+=1


        result = int(stack[0])
        i = 1
        stack_length = len(stack)
        while i < stack_length - 1:
            if stack[i] == '+':
                result += int(stack[i+1])
            elif stack[i] == '-':
                print(int(stack[i+1]))
                result -= int(stack[i+1])

            i += 2

        return result
