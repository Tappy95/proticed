from datetime import datetime, timedelta

time_utc = "2020-01-06T16:00:00.000Z"
date = datetime.strptime(time_utc, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours=8)
print(date)

