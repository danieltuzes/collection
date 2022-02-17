import calendar
import datetime
from dateutil import relativedelta

start_str = "1-03-2022"
end_str = "20-12-2024"

start = datetime.datetime.strptime(start_str, "%d-%m-%Y")
end = datetime.datetime.strptime(end_str, "%d-%m-%Y")

days = []


while start.year <= end.year and start.month <= end.month:
    if start.year == end.year and start.month == end.month:
        days.append(end.day - start.day)
    else:
        days.append(calendar.monthrange(
            start.year, start.month)[1]-start.day+1)
    start = start.replace(day=1)
    start += relativedelta.relativedelta(months=1)

print(*days)
