import datetime
import time
today = datetime.date.today()
print(int(round(time.time() * 1000)))
print(type(today))
print(str(datetime.datetime.now().replace(microsecond=0)))


a={
    "a":1
}
print(a.get("a"))

