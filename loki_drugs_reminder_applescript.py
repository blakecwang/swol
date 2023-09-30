#!/usr/bin/env python

"""
Remind me to give Loki his drugs on the second Monday of each month at 11am
"""

import datetime
from random import randrange


DATE_FORMAT = "%A, %-m/%-d/%Y at %-I:%M %p"  # Wednesday, 10/12/2022 at 5:41 PM

today = datetime.date.today()
day = datetime.datetime(today.year, today.month, 1, 11)

date_strs = []
for i in range(24):
    # go to second Monday
    monday_count = 0
    while monday_count < 2:
        if day.weekday() == 0:  # 0 corresponds to Monday
            monday_count += 1
        day += datetime.timedelta(days=1)
    day -= datetime.timedelta(days=1)

    date_strs.append(day.strftime(DATE_FORMAT))

    # go to 1st of next month
    month = day.month
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
        'make new reminder at end with properties {name:"Loki Drugs", due date:date "' +
        date_str +
        '"}'
    )

print(
    '\tend tell\n' +
    'end tell\n'
)
