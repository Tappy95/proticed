# from datetime import datetime, timedelta
#
# time_utc = "2020-01-06T16:00:00.000Z"
# date = datetime.strptime(time_utc, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=8)
# print(date)
# complete_list = []
# a = []
# name_list = ["a","b"]
# id_list = [1,2]
# try:
#     for i in range(3):
#         complete_list.append({"name": name_list.pop(0), "id": id_list.pop(0)})
#     a.append(complete_list)
# except Exception as e:
#     # logger.info(e)
#     a.append(complete_list)
#
# print(complete_list)
from operator import itemgetter

a = [
            {
                "date": "2020-03-13",
                "sold": "0",
                "sold_ring": "0.0",
                "sold_diff": "0"
            },
            {
                "date": "2019-12-23",
                "sold": "0",
                "sold_ring": "0",
                "sold_diff": "0"
            },
            {
                "date": "2019-12-13",
                "sold": "0",
                "sold_ring": "0",
                "sold_diff": "0"
            }
        ]
a.sort(key=itemgetter('date'))
print(a)
