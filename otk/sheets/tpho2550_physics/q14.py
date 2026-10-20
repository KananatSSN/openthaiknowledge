"""Lab 2, part 2.1: T = 2 pi sqrt((M + m_s)/k) makes T^2 linear in M with slope 4 pi^2/k, so k = 4 pi^2/slope. Adapted: synthetic slope of T^2 against M (s^2/kg); N/m."""

from math import pi, sqrt


def solve(slope=0.8, intercept=0.02):
    return 4 * pi**2 / slope


def check(slope=0.8, intercept=0.02):
    # Rebuild two periods from the line and recover k from them directly.
    m1, m2 = 0.2, 0.6
    t1, t2 = sqrt(slope * m1 + intercept), sqrt(slope * m2 + intercept)
    return 4 * pi**2 * (m2 - m1) / (t2**2 - t1**2)


PARAMS = {"slope": 0.8, "intercept": 0.02}
VARIANTS = [{"slope": 0.4}, {"slope": 1.6, "intercept": 0.05}, {"intercept": 0.0}]
ANSWER = 49.348022005446786
TOL = 1e-9
