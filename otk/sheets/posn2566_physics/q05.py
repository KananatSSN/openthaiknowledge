"""MC5: Maxwell distribution N(v) = A v^2 exp(-B v^2 / T): starts at zero with zero slope, one peak, decays to zero (answer 4). Adapted quantity: the peak speed sqrt(T/B)."""

from math import exp, sqrt


def solve(temperature=400, b=4):
    return sqrt(temperature / b)


def check(temperature=400, b=4):
    # Golden-section search for the maximum of v^2 exp(-B v^2/T).
    f = lambda v: v * v * exp(-b * v * v / temperature)
    lo, hi = 0.0, 10 * sqrt(temperature / b)
    ratio = (sqrt(5) - 1) / 2
    for _ in range(300):
        a = hi - ratio * (hi - lo)
        c = lo + ratio * (hi - lo)
        if f(a) < f(c):
            lo = a
        else:
            hi = c
    return (lo + hi) / 2


PARAMS = {"temperature": 400, "b": 4}
VARIANTS = [{"temperature": 900, "b": 1}, {"b": 25}, {"temperature": 300, "b": 3}]
TOL = 1e-7
ANSWER = 10.0
