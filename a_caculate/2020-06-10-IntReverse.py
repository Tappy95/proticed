class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        if x < 0:
            y = -int(str(-x)[::-1])
        else:
            y = int(str(x)[::-1])
        return y if -2 ** 31 <= y <= 2 ** 31 - 1 else 0


a = Solution()
print(a.reverse(534236469))
