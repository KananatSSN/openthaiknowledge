"""Theory 1.3 f), g): a tube m' welded to a half cylinder m (cm 4R/(3 pi) from the axis) has its cm at k'R, k' = mk/(m + m'); starting from rest flat face up it rolls all the way down if sin(theta) >= k'(1 - cos(beta))/beta for every beta, i.e. theta_min = arcsin(k' sin theta0) with theta0 = tan(theta0/2), 2.33 rad. Adapted: both masses (kg) vary; returns degrees."""

from math import asin, degrees, pi, sin, tan


def solve(tube=1.0, half=0.5):
    from otk.sheets.tpho2564_physics._shared import HALF_DISC, bisect

    k = half * HALF_DISC / (half + tube)
    root = bisect(lambda x: x - tan(x / 2), 2.0, 3.0)
    return degrees(asin(k * sin(root)))


def check(tube=1.0, half=0.5):
    from math import cos

    from otk.sheets.tpho2564_physics._shared import HALF_DISC, golden_min

    k = half * HALF_DISC / (half + tube)
    worst = golden_min(lambda b: -(1 - cos(b)) / b, 0.1, 2 * pi)
    return degrees(asin(k * (1 - cos(worst)) / worst))


PARAMS = {"tube": 1.0, "half": 0.5}
VARIANTS = [{"half": 2.0}, {"tube": 0.2}, {"half": 0.1}]
ANSWER = 5.883814376854091
TOL = 1e-6
