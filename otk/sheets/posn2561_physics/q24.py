"""Written4 figure: smooth incline lengthL angle30deg, A releasedrest fromtop, B launched uphill frombottom simultaneously. They meet at midpoint. Initial B speed sqrt(L g sin theta)."""

from math import sqrt


def solve(length=10, sine=0.5, g=9.8):
    return sqrt(length * g * sine)


def check(length=10, sine=0.5, g=9.8):
    # Find the upper block's midpoint arrival numerically, then shoot B.
    acceleration = g * sine
    lo, hi = 0.0, 100.0
    for _ in range(100):
        time = (lo + hi) / 2
        if length - acceleration * time * time / 2 > length / 2:
            lo = time
        else:
            hi = time
    time = (lo + hi) / 2
    lo, hi = 0.0, 1000.0
    for _ in range(100):
        speed = (lo + hi) / 2
        position = speed * time - acceleration * time * time / 2
        if position < length / 2:
            lo = speed
        else:
            hi = speed
    return (lo + hi) / 2


PARAMS = {"length": 10, "sine": 0.5, "g": 9.8}
VARIANTS = [{"length": 20}, {"sine": 0.6}, {"g": 10}]
ANSWER = 7.0
