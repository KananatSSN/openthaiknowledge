"""Experiment 1b: ln(T - Ta) falls linearly with slope -1/beta; from two readings beta = (t2 - t1)/ln((T1 - Ta)/(T2 - Ta)). Seconds."""

from math import exp, log


def solve(room=30, first=90, second=60, gap=600):
    return gap / log((first - room) / (second - room))


def check(room=30, first=90, second=60, gap=600):
    # Bisect on beta so the cooling law carries the first reading to the
    # second after `gap` seconds.
    lo, hi = 1e-6, 1e9
    for _ in range(300):
        beta = (lo + hi) / 2
        predicted = room + (first - room) * exp(-gap / beta)
        if predicted < second:
            lo = beta
        else:
            hi = beta
    return (lo + hi) / 2

PARAMS = {"room": 30, "first": 90, "second": 60, "gap": 600}
VARIANTS = [{"second": 45}, {"room": 20, "first": 100, "second": 60, "gap": 300}, {"gap": 1200}]
ANSWER = 865.6170245333781
