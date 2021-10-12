import math

THIRD = 1.0/3


def float_mod(num):
    return (int(num * 1000) % 1000) / 1000.0


def ceil_third(num):
    if float_mod(num) < THIRD:
        return math.floor(num)
    return math.ceil(num)


def round_duration(num):
    return ceil_third(num * 4.0) / 4.0


def ceil_duration(num):
    return math.ceil(num * 4.0) / 4.0


def floor_duration(num):
    return math.floor(num * 4.0) / 4.0
