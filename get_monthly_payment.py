#!/usr/bin/env python
from __future__ import annotations

import argparse


def get_monthly_payment(
    annual_rate: float,
    loan_amount: int,
    months: int,
) -> float:
    monthly_rate = annual_rate / 12
    factor = (1 + monthly_rate) ** months
    top = loan_amount * monthly_rate * factor
    bottom = factor - 1
    return top / bottom


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--annual-rate", type=float, required=True)
    parser.add_argument("-a", "--loan-amount", type=int, required=True)
    parser.add_argument("-n", "--months", type=int, required=True)
    pargs = parser.parse_args()
    monthly_payment = get_monthly_payment(pargs.annual_rate, pargs.loan_amount, pargs.months)
    total = round(monthly_payment * pargs.months, 2)
    monthly_payment = round(monthly_payment, 2)
    print(f"{monthly_payment=} {total=}")
