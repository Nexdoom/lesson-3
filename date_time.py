# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
import locale
import calendar


locale.setlocale(locale.LC_ALL, "russian")


def get_months(src_date,months):
    month = src_date.month - 1 + months
    year = src_date.year + month // 12
    month = month % 12 + 1
    day = min(src_date.day,calendar.monthrange(year,month)[1])
    return date(year,month,day)


dt_now = datetime.now()
dt_current = dt_now.strftime("%A-%d-%B-%Y")
print("сегодняшняя дата: {}".format(dt_current))

delta = timedelta(days=1)
yday = dt_now - delta
yday = yday.strftime("%A-%d-%B-%Y")
print("вчера было: {}".format(yday))


somedate = date.today()
somedate = get_months(somedate, -1)
somedate = somedate.strftime("%A-%d-%B-%Y")
print("Месяц назад было: {}".format(somedate))



date_str = "01/01/17 12:10:03.234567"
dt = datetime.strptime(date_str, "%m/%d/%y %H:%M:%S.%f")
print(dt)
