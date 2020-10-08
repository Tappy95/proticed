import json

dict1 = {
    "xxxx": 3,
    "xxxxx": 1,
    "xxxx1": 2,
    "xxxx2": 4
}
b = [{"asin": k, "rank": v} for k, v in dict1.items()]
# a = [{"asin": "xxx", "rank": 3}, {"asin": "xxxx", "rank": 1}, {"asin": "xxxxx", "rank": 2}]
newlist = sorted(b, key=lambda k: k['rank'])
print(newlist)
