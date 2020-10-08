import time
from datetime import datetime, timedelta

now = datetime.now()
zeroToday = now - timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                            microseconds=now.microsecond) + timedelta(days=1)
delta = zeroToday - now
# time.sleep(4)
# start_time = datetime.now()
# if start_time - now > timedelta(seconds=3):
#     print("geieieieie")
# else:
#     print(now-start_time)
print(now)
print(zeroToday)
print(delta.total_seconds())