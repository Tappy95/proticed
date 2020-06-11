class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        parenttheses_dict = {
            "(": ")",
            "[": "]",
            "{": "}",
            "_": "_"
        }
        stack = ["_"]
        for i in s:
            if i in parenttheses_dict:
                stack.append(i)
            elif parenttheses_dict[stack.pop()] != i:
                return False
        return len(stack) == 1


a = Solution()
print(a.isValid("()"))
