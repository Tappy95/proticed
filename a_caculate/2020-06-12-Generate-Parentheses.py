class Solution(object):
    def generateParenthesis(self, n):
        """
        :type n: int
        :rtype: List[str]
        """
        parent1 = "()"
        start_result = ""
        for i in range(n):
            start_result += parent1

        print(start_result)

a = Solution()
a.generateParenthesis(3)