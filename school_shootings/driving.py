#!/usr/bin/env python

# 40,000 annual fatalities
# 330 million drivers
# 13.8 years
driving_risk = 1 - ((1 - (40000 / 330000000)) ** 13.8)

school_shooting_risk =  0.000043636363636363636364

factor = driving_risk / school_shooting_risk
breakpoint()
