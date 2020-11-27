# coding=utf-8
import time
from datetime import datetime, timedelta, date

# now = int(time.time())
# zeroToday = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
#                             microseconds=now.microsecond) + timedelta(days=1)
# delta = zeroToday - now
# time.sleep(4)
# start_time = datetime.now()
# if start_time - now > timedelta(seconds=3):
#     print("geieieieie")
# else:
#     print(now-start_time)
# print(now)
# print(zeroToday)
# print(delta.total_seconds())
# time1 = 0
# time2 = datetime.fromtimestamp(time1)
# time3 = time.strftime("%Y%m%d%H%M%S", time2)
# print(time2)
# cur = time.time()
# a = cur - cur % 86400 - 20 * 3600
# print(a)
# 获取当前时间
now = datetime.now()
# 获取今天零点
zeroToday = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,microseconds=now.microsecond)
# 获取23:59:59
lastToday = zeroToday + timedelta(hours=23, minutes=59, seconds=59)
print(zeroToday,lastToday)
print(time.mktime(zeroToday.timetuple())*1000)
print(time.mktime(lastToday.timetuple()))
print(type(time.mktime(lastToday.timetuple())))

# a = ['2020-10-16', '2020-10-15', '2020-10-17']
# b = sorted(a)
# print(b)
# a = [1,2,3,4]
# print(a[1:])
# print(a[:1])
# print(a[1:]+a[:1])
# from datetime import date
# f_date = date(1, 1, 1)
# l_date = date(2020, 10, 22)
# delta = l_date - f_date
# print(delta.days)
#

#
#
# print(float("0.85") * int("8"))

# today = date.today()
# d2 = today - timedelta(days=8)
# # dd/mm/YY
# d1 = today.strftime("%Y-%m-%d")
# d2 = d2.strftime("%Y-%m-%d")
# print(d1)
# print(d2)
# print(int(time.time()*1000))
# if "0":
#     print("--------------")
# print(datetime(2020,11,9))

def date_range(start_time, end_time, effect_time):
    dates = []
    # dt = datetime.strptime(start_time, "%Y-%m-%d")
    dt = start_time
    date1 = start_time
    while date1 <= end_time:
        dates.append(date1.strftime("%Y-%m-%d"))
        dt = dt + timedelta(1)
        date1 = dt
    for e_time in effect_time:
        if e_time in dates:
            dates.remove(e_time)

    return dates

# print(date_range(datetime(2020,11,1), datetime(2020,11,24), []))


from datetime import datetime
days = 738075
print(datetime.fromordinal(days - 365))