class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if not strs:
            return ""
        count = min([len(i) for i in strs])
        list_1 = [[] for i in range(count)]
        for j in strs:
            for i in range(count):
                list_1[i].append(j[i])
        real_result = ""
        for idx, x in enumerate(list_1):
            if len(set(x)) != 1:
                return real_result
            elif len(set(x)) == 1:
                real_result += "".join(set(x))
        return real_result

    def longestCommonPrefix1(self, strs):
        ans = ''
        for i in zip(*strs):
            if len(set(i)) == 1:
                ans += i[0]
            else:
                break
        return ans


a = Solution()
print(a.longestCommonPrefix([""]))
