class Solution(object):
    def twoSum1(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        for i, element1 in enumerate(nums):
            for j, element2 in enumerate(nums):
                if element1 + element2 == target and i != j:
                    return sorted([i, j], reverse=False)
        return False

    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        hashmap = {}
        for ind, value in enumerate(nums):
            if target - value in hashmap:
                return [hashmap[target - value], ind]
            else:
                hashmap[value] = ind


a = Solution()
print(a.twoSum([3, 2, 4], 6))
