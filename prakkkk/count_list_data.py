import time
from datetime import datetime
from itertools import groupby
from random import random, randint

# 分组算法
# list1 = []
# for i in range(10):
#     list1.append({"value":randint(1, 20)})
# list2 = sorted(list1, key=lambda a: a['value'])
# print(list2)
# for k, g in groupby(list2, key=lambda x: x['value'] // 5):
#     a = list(g)
#     print(k, a)
#     print('{}--{}:{}'.format(k * 5, (k + 1) * 5 - 1, len(a)))

groups = []
uniquekeys = []
list1 = [1,2,3,4,5,6,7,8,9]
data1 = sorted(list1)
print(data1)
for k, g in groupby(data1, lambda x: x // 2):
    a = list(g)
    b = k
    print(list(a))
    groups.append(list(a))  # Store group iterator as a list
    uniquekeys.append(b)
    print('{}--{}:{}'.format(b * 2, (b + 1) * 2, len(a)))
print(groups, uniquekeys)


# a =1604380370063
# print(datetime.fromtimestamp(a/1000))