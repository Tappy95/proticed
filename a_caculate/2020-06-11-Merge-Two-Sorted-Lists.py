# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def mergeTwoLists(self, l1, l2):
        # 创建哑节点作为 结果链表 的开头
        dummy = ListNode(0)
        # 有个游标，标识 结果链表 的结尾
        move = dummy
        # l1 和 l2 都未遍历结束
        while l1 and l2:
            # 如果 l1 的数值比较小
            if l1.val <= l2.val:
                # 把 l1 头部节点拼接到 结果链表 的结尾
                move.next = l1
                # l1 指向下一个节点
                l1 = l1.next
            else:
                # 把 l2 头部节点拼接到 结果链表 的结尾
                move.next = l2
                # l2 指向下一个节点
                l2 = l2.next
            # 移动 结果链表 的结尾指针
            move = move.next
        # l1 或者 l2 尚未使用完，拼接到 结果链表 的最后
        move.next = l1 if l1 else l2
        # 返回哑节点的下一个位置
        return dummy.next

