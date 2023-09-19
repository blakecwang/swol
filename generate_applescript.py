#!/usr/bin/env python


from datetime import datetime, timedelta
from random import randrange


# blake
SHEET_LINK = "https://docs.google.com/spreadsheets/d/1chUvK9Bv5NALVYzXa47DarZjs_RM_NcFEA1KCaJwXRQ/edit?usp=sharing"
LOWER_BOUND = 7   # 7am
UPPER_BOUND = 21  # 9pm

# amber
#SHEET_LINK = "https://docs.google.com/spreadsheets/d/1tjkGfl6iQwzfSq4YFpwD04Kt2fDr6ybChwJtBqOJxSs/edit?usp=sharing"
#LOWER_BOUND = 7   # 7am
#UPPER_BOUND = 20  # 8pm

DATE_FORMAT = "%A, %-m/%-d/%Y at %-I:%M %p"  # Wednesday, 10/12/2022 at 5:41 PM


minutes_per_day = (UPPER_BOUND - LOWER_BOUND) * 60

# start today
curr = datetime.now() - timedelta(days=1)
curr = datetime(curr.year, curr.month, curr.day, LOWER_BOUND)

date_strs = []
for i in range(120):
    minutes = randrange(minutes_per_day)
    date_str = (curr + timedelta(minutes=minutes)).strftime(DATE_FORMAT)
    date_strs.append(date_str)
    curr += timedelta(days=1)

print('---- SPREADSHEET ----')
for date_str in date_strs:
    print(date_str)

print(
    '\n\n\n\n---- APPLESCRIPT ----\n' +
    'tell application "Reminders"\n' +
    '\tset mylist to list "Reminders"\n' +
    '\ttell mylist'
)

for date_str in date_strs:
    print(
        '\t\t' +
        'make new reminder at end with properties {name:"Collect data for ' +
        date_str +
        ': ' +
        SHEET_LINK +
        '", due date:date "' +
        date_str +
        '"}'
    )

print(
    '\tend tell\n' +
    'end tell\n'
)
