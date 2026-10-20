"""Lab 2, part 2.2: the line T^2 = (4 pi^2/k)(M + m_s) cuts the T^2 axis at (4 pi^2/k) m_s, so m_s = intercept/slope. Adapted: synthetic slope and intercept; kg."""

from math import sqrt


def solve(slope=0.8, intercept=0.02):
    return intercept / slope


def check(slope=0.8, intercept=0.02):
    # Extrapolate two readings to T = 0: the mass axis is cut at M = -m_s.
    m1, m2 = 0.2, 0.6
    y1, y2 = sqrt(slope * m1 + intercept) ** 2, sqrt(slope * m2 + intercept) ** 2
    zero = m1 - y1 * (m2 - m1) / (y2 - y1)
    return -zero


PARAMS = {"slope": 0.8, "intercept": 0.02}
VARIANTS = [{"slope": 0.4}, {"slope": 1.6, "intercept": 0.05}, {"intercept": 0.1}]
ANSWER = 0.024999999999999998
TOL = 1e-9
