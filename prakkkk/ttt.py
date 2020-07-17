import datetime


def date_range(start_time, end_time, effect_time):
    dates = []
    dt = datetime.datetime.strptime(start_time, "%Y-%m-%d")
    date = start_time[:]
    while date <= end_time:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    for e_time in effect_time:
        if e_time in dates:
            dates.remove(e_time)

    return dates


print(date_range('2020-02-03','2020-02-07',[]))