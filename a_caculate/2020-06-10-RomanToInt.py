d = {'I': 1, 'IV': 3, 'V': 5, 'IX': 8, 'X': 10, 'XL': 30, 'L': 50, 'XC': 80, 'C': 100, 'CD': 300, 'D': 500,
     'CM': 800, 'M': 1000}


class Solution(object):

    def romanToInt1(self, s):
        """
        :type s: str
        :rtype: int
        """
        roman_dict = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000
        }

        print(s[0:1])
        fake_result = 0
        for element in s:
            fake_result += roman_dict[element]
        if "IV" in s or "IX" in s:
            fake_result -= 2 * roman_dict['I']
        if "XL" in s or "XC" in s:
            fake_result -= 2 * roman_dict['X']
        if "CD" in s or "CM" in s:
            fake_result -= 2 * roman_dict['C']
        return fake_result

    def romanToInt2(self, s):

        return sum(d.get(s[max(i - 1, 0):i + 1], d[n]) for i, n in enumerate(s))

    def romanToInt3(self, s):
        result = 0
        for i,n in enumerate(s):
            a = s[max(i-1,0):i+1]
            b=d.get(a,d[n])
            print(a)
            print(b)
            result += b
        return result

a = Solution()
# # a.romanToInt("MMCMLXXXIV")
# print(a.romanToInt1("III"))
# a = Solution
print(a.romanToInt3("MMCMLXXXIV"))
