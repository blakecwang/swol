#!/usr/bin/env python

"""
Remind me to pay Nicolas on the last Friday of each month at 11am.
"""

import datetime
from random import randrange


DATE_FORMAT = "%A, %-m/%-d/%Y at %-I:%M %p"  # Wednesday, 10/12/2022 at 5:41 PM

today = datetime.date.today()
day = datetime.datetime(today.year, today.month, 1, 11)

date_strs = []
for i in range(24):
    month = day.month

    # go forward to end of month
    while day.month == month:
        day += datetime.timedelta(days=1)
    day -= datetime.timedelta(days=1)

    # go back to friday
    while day.weekday() != 4:  # 4 corresponds to Friday (Monday is 0)
        day -= datetime.timedelta(days=1)

    date_strs.append(day.strftime(DATE_FORMAT))

    # go to next month
    while day.month == month:
        day += datetime.timedelta(days=1)


print(
    '\n\n\n\n---- APPLESCRIPT ----\n' +
    'tell application "Reminders"\n' +
    '\tset mylist to list "Reminders"\n' +
    '\ttell mylist'
)

for date_str in date_strs:
    print(
        '\t\t' +
        'make new reminder at end with properties {name:"Pay Nicolas", due date:date "' +
        date_str +
        '"}'
    )

print(
    '\tend tell\n' +
    'end tell\n'
)
