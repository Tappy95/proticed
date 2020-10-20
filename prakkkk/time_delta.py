import time
from datetime import datetime, timedelta

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
# time1 = 1602691200.000
# time2 = datetime.fromtimestamp(time1)
# time3 = time.strftime("%Y%m%d%H%M%S", time2)
# print(time2)
# cur = time.time()
# a = cur - cur % 86400 - 20 * 3600
# print(a)


# a = ['2020-10-16', '2020-10-15', '2020-10-17']
# b = sorted(a)
# print(b)
a = [1,2,3,4]
print(a[1:])
print(a[:1])
print(a[1:]+a[:1])