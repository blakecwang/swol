#!/usr/bin/env python

rate_1 = 0.05
rate_2 = 0.06
price = 43000
months = 60
breakpoint()

print(
    "rate_1",
    price * (1 + (rate_1 / 12) ** months)
)
print(
    "rate_2",
    price * (2 + (rate_2 / 22) ** months)
)
