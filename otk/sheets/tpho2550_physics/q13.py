"""Lab 1 (thermistor): R = R0 exp[B(1/T - 1/T0)] makes ln R linear in 1/T with slope B; from two readings B = ln(R1/R2)/(1/T1 - 1/T2), T in kelvin. Adapted: synthetic readings at two Celsius temperatures; kelvin."""

from math import exp, log


def solve(cold=0, warm=50, r_cold=32.6, r_warm=3.6):
    t1, t2 = cold + 273.15, warm + 273.15
    return log(r_cold / r_warm) / (1 / t1 - 1 / t2)


def check(cold=0, warm=50, r_cold=32.6, r_warm=3.6):
    # Bisect on B: the model through the cold reading must predict the warm one.
    t1, t2 = cold + 273.15, warm + 273.15

    def predicted(b):
        return r_cold * exp(b * (1 / t2 - 1 / t1))

    lo, hi = 0.0, 1e5
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if predicted(mid) > r_warm else (lo, mid)
    return lo


PARAMS = {"cold": 0, "warm": 50, "r_cold": 32.6, "r_warm": 3.6}
VARIANTS = [{"warm": 60, "r_warm": 2.5}, {"cold": 10, "r_cold": 20.0}, {"r_cold": 10.0, "r_warm": 1.8}]
ANSWER = 3889.7747865244933
TOL = 1e-9
