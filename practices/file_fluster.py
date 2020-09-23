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
# from operator import itemgetter
#
# a = [
#             {
#                 "date": "2020-03-13",
#                 "sold": "0",
#                 "sold_ring": "0.0",
#                 "sold_diff": "0"
#             },
#             {
#                 "date": "2019-12-23",
#                 "sold": "0",
#                 "sold_ring": "0",
#                 "sold_diff": "0"
#             },
#             {
#                 "date": "2019-12-13",
#                 "sold": "0",
#                 "sold_ring": "0",
#                 "sold_diff": "0"
#             }
#         ]
# a.sort(key=itemgetter('date'))
# print(a)
# merchant_result = {
#     'merchant_id': 'merchant_id',
#     'site': 'site',
#     'merchant_name': 'merchant_name',
#     'logo_url': '',
#     'description': '',
#     'merchant_info': '',
#     '30d_positive': 0,
#     '30d_neutral': 0,
#     '30d_negative': 0,
#     '30d_count': 0,
#     '90d_positive': 0,
#     '90d_neutral': 0,
#     '90d_negative': 0,
#     '90d_count': 0,
#     '12m_positive': 0,
#     '12m_neutral': 0,
#     '12m_negative': 0,
#     '12m_count': 0,
#     'lt_positive': 0,
#     'lt_neutral': 0,
#     'lt_negative': 0,
#     'lt_count': 0,
#     'update_time': 'update_time'
# }
# merchant_values = "(" + ','.join(
#     [str(value) if value or value == 0 else '" "' for value in merchant_result.values()]) + ")"
# merchant_values.replace(",0", ",9")
# a = ",".join([merchant_values.replace(",0", ",9") for x in range(5)])
# print(a)
# b = " "
# if b == " ":
#     print("amd yes")

# INSERT INTO amazon_merchant (merchant_id, site, merchant_name, logo_url, description, merchant_info, 30d_positive,30d_neutral,30d_negative,30d_count,90d_positive,90d_neutral,90d_negative,90d_count,12m_positive,12m_neutral,12m_negative,12m_count,lt_positive,lt_neutral,lt_negative,lt_count,update_time) VALUES
# (" ","de"," ",' ',' ',' ',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,"2020-09-02 00:01:00")
# ON DUPLICATE KEY UPDATE merchant_id = VALUES(merchant_id) ,site = VALUES(site);


import asyncio
import copy
import json

filename = "2020-09-14_us"

sites = ['us', 'uk']


class FileBuffer(object):

    def __init__(self, name, max_size, us_file, uk_file, au_file, de_file):
        self.name = name
        self.max_size = max_size
        self.size = 0
        self.us_file = us_file
        self.uk_file = uk_file
        self.au_file = au_file
        self.de_file = de_file
        self.body = {
            "us": [],
            "uk": [],
            "au": [],
            "de": [],
        }

    async def push(self, data):
        data = data if data else None
        site = data.pop('site')
        _datas = (data,)
        _size = len(data) + 1
        if _size + self.size > self.max_size:
            await self.flush()
        self.body[site].append(_datas)
        self.size += _size

    async def flush(self):
        if self.size:
            row_list_us = "\n".join(
                ['\t'.join([ele for ele in data.values()]) for datas in self.body["us"] for data in datas]) + "\n"\
                if len(self.body["us"]) > 0 else ""
            row_list_uk = "\n".join(
                ['\t'.join([ele for ele in data.values()]) for datas in self.body["uk"] for data in datas]) + "\n"\
                if len(self.body["uk"]) > 0 else ""
            row_list_au = "\n".join(
                ['\t'.join([ele for ele in data.values()]) for datas in self.body["au"] for data in datas]) + "\n"\
                if len(self.body["au"]) > 0 else ""
            row_list_de = "\n".join(
                ['\t'.join([ele for ele in data.values()]) for datas in self.body["de"] for data in datas]) + "\n"\
                if len(self.body["de"]) > 0 else ""
            # row_data = "\n".join(row_list) + "\n"
            self.us_file.write(row_list_us)
            self.uk_file.write(row_list_uk)
            self.au_file.write(row_list_au)
            self.de_file.write(row_list_de)
            # print("{} size: {}, count: {}, avg_size: {}".format(
            #     self.name, len(row_data), len(self.body), len(row_data) / len(self.body)))
            self.size = 0
            self.body = {
                "us": [],
                "uk": [],
                "au": [],
                "de": [],
            }


async def coco():
    with open('./us.txt', 'a') as f1, open('./uk.txt', 'a') as f2, \
            open('./au.txt', 'a') as f3, open('./de.txt', 'a') as f4:
        buffer = FileBuffer('f1', 20, f1, f2, f3, f4)
        for idx, i in enumerate(range(1)):
            dct = {
                "item_id": "123",
                "category_path": "123:1234:45234",
                "title": "fuck the java",
                "site": "uk"
            }
            await buffer.push(dct)
        else:
            await buffer.flush()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(coco())
    loop.close()
