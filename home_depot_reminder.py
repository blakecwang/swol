#!/usr/bin/env python

"""
Remind me that there is a home depot kids workshop on the first Saturday of every month.
But remind me on the preceeding Thursday.
"""

import datetime


DATE_FORMAT = "%A, %-m/%-d/%Y at %-I:%M %p"  # Wednesday, 10/12/2022 at 5:41 PM

today = datetime.date.today()
day = datetime.datetime(today.year, today.month, 1, 12)

date_strs = []
for i in range(24):
    # go to first Saturday
    saturday_count = 0
    while saturday_count == 0:
        if day.weekday() == 5:  # 5 corresponds to Monday
            saturday_count += 1
        day += datetime.timedelta(days=1)
    day -= datetime.timedelta(days=1)

    date_strs.append((day - datetime.timedelta(days=2)).strftime(DATE_FORMAT))

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
        'make new reminder at end with properties {name:"Home Depot workshop this Saturday", due date:date "' +
        date_str +
        '"}'
    )

print(
    '\tend tell\n' +
    'end tell\n'
)
