#!/usr/bin/env python
import decimal
import math

decimal.getcontext().prec = 100000

def leibniz(n):
    pi = decimal.Decimal(1)
    for i in range (1,n):
        pi += ((-1) ** i ) * (decimal.Decimal(1) / (2 * i + 1))
    return pi * 4

print(leibniz(1000))
