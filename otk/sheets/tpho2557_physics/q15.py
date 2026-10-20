"""Lab part 3: the same line v_T/cos(theta) = (mg/b) tan(theta) - (mg/b) mu crosses the axis at -(mg/b) mu, so mu = -intercept/slope; the solution's 0.0666/0.366 gives 0.18. Adapted with synthetic heights (cm) of a 70 cm incline and times (s) over 20 cm; returns mu."""

from otk.sheets.tpho2557_physics.q14 import _points


def solve(heights=(24.0, 25.2, 26.4, 27.6, 28.8, 30.0, 31.2), times=(3.69, 3.35, 3.04, 2.84, 2.55, 2.33, 2.17), run=0.70, stretch=0.20):
    xs, ys = _points(heights, times, run, stretch)
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return -(my - slope * mx) / slope


def check(heights=(24.0, 25.2, 26.4, 27.6, 28.8, 30.0, 31.2), times=(3.69, 3.35, 3.04, 2.84, 2.55, 2.33, 2.17), run=0.70, stretch=0.20):
    # The fitted line's root: tan(theta) at which the magnet would just stop.
    from otk.sheets.tpho2557_physics._shared import bisect, line

    slope, intercept = line(*_points(heights, times, run, stretch))
    return bisect(lambda x: slope * x + intercept, -5.0, 5.0)


PARAMS = {"heights": (24.0, 25.2, 26.4, 27.6, 28.8, 30.0, 31.2), "times": (3.69, 3.35, 3.04, 2.84, 2.55, 2.33, 2.17), "run": 0.70, "stretch": 0.20}
VARIANTS = [
    {"times": (3.20, 2.95, 2.70, 2.50, 2.30, 2.15, 2.00)},
    {"heights": (22.0, 23.5, 25.0, 26.5, 28.0, 29.5, 31.0)},
    {"times": (4.0, 3.5, 3.1, 2.8, 2.55, 2.35, 2.2)},
]
ANSWER = 0.2000725469532395
TOL = 1e-9
