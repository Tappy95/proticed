# Definition for singly-linked list.
# A single node of a singly linked list
class Node:
    # constructor
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


# A Linked List class with a single head node
class LinkedList:
    def __init__(self):
        self.head = None

    # insertion method for the linked list
    def insert(self, data):
        newNode = Node(data)
        if (self.head):
            current = self.head
            while (current.next):
                current = current.next
            current.next = newNode
        else:
            self.head = newNode

    # print method for the linked list
    def printLL(self):
        current = self.head
        while (current):
            print(current.data)
            current = current.next


# Singly Linked List with insertion and print methods
LL = LinkedList()
LL.insert(3)
LL.insert(4)
LL.insert(5)
LL.printLL()


class Solution:
    def mergetwolists(self, l1, l2):
        if not l1:
            return l2  # 终止条件，直到两个链表都空
        if not l2:
            return l1
        if l1.data <= l2.data:  # 递归调用
            l1.next = self.mergetwolists(l1.next, l2)
            return l1
        else:
            l2.next = self.mergetwolists(l1, l2.next)
            return l2


# a = Solution()
# data1 = [1, 1, 2, 3, 31]
# data2 = [1, 1, 4, 5, 19]
# l1 = Linklist(data1)
# l2 = Linklist(data2)
# for i in l1:
#     print(i.data)
# print(a.mergetwolists(l1, l2))
