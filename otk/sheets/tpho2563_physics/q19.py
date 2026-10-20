"""Lab part 3.2: T = 2 mu N W1 sqrt(pi/(4k)) sqrt(d) exp(k/d) + T0, so ln((T - T0)/sqrt(d)) against 1/d is a straight line of slope k. The solution's pulls at d = 1.5 to 3.0 cm (T0 = 0) give k = 0.042 m. Adapted: the readings and T0 vary; returns metres."""

from math import log, sqrt

GAPS = (0.015, 0.017, 0.020, 0.025, 0.030)
PULLS = (30.17, 20.42, 20.76, 11.59, 10.46)


def solve(gaps=GAPS, pulls=PULLS, other=0.0):
    from otk.sheets.tpho2563_physics._shared import line

    return line([1 / d for d in gaps], [log((t - other) / sqrt(d)) for d, t in zip(gaps, pulls)])[0]


def check(gaps=GAPS, pulls=PULLS, other=0.0):
    from otk.sheets.tpho2563_physics._shared import centred_line

    return centred_line([1 / d for d in gaps], [log((t - other) / sqrt(d)) for d, t in zip(gaps, pulls)])[0]


PARAMS = {"gaps": GAPS, "pulls": PULLS, "other": 0.0}
VARIANTS = [{"other": -0.1}, {"pulls": (40.0, 27.0, 18.5, 12.9, 10.1)}, {"gaps": (0.016, 0.018, 0.021, 0.025, 0.031)}]
ANSWER = 0.041890822538660485
TOL = 1e-9
