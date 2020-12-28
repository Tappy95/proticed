import random

# ad = {str(i):0 for i in range(10)}
# for a in range(999):
#     d = random.randint(0,9)
#     ad[str(d)] += 1
# print(ad)
a = {}
for idx, i in enumerate(range(6)):
    a[str(i)] = []
    print(idx)
print(a)