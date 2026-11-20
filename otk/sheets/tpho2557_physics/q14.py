"""Lab part 3: at terminal speed m g sin(theta) = b v_T + mu m g cos(theta), so v_T/cos(theta) = (mg/b)(tan theta - mu), a line in tan(theta) with slope mg/b; the solution's slope 0.366 gives b = 0.47 kg/s for the 17.4 g magnet. Adapted with synthetic heights (cm) of a 70 cm incline and times (s) over 20 cm; returns b in kg/s with g = 9.8."""

from math import sqrt


def _points(heights, times, run, stretch):
    xs, ys = [], []
    for h, t in zip(heights, times):
        s = h / (run * 100)
        c = sqrt(1 - s * s)
        xs.append(s / c)
        ys.append(stretch / t / c)
    return xs, ys


def solve(heights=(24.0, 25.2, 26.4, 27.6, 28.8, 30.0, 31.2), times=(3.69, 3.35, 3.04, 2.84, 2.55, 2.33, 2.17), mass=17.4, run=0.70, stretch=0.20, g=9.8):
    xs, ys = _points(heights, times, run, stretch)
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return mass * 1e-3 * g / slope


def check(heights=(24.0, 25.2, 26.4, 27.6, 28.8, 30.0, 31.2), times=(3.69, 3.35, 3.04, 2.84, 2.55, 2.33, 2.17), mass=17.4, run=0.70, stretch=0.20, g=9.8):
    from otk.sheets.tpho2557_physics._shared import line

    slope, _ = line(*_points(heights, times, run, stretch))
    # The time constant route: tau = m/b with b = mg/slope.
    tau = slope / g
    return mass * 1e-3 / tau


PARAMS = {"heights": (24.0, 25.2, 26.4, 27.6, 28.8, 30.0, 31.2), "times": (3.69, 3.35, 3.04, 2.84, 2.55, 2.33, 2.17), "mass": 17.4, "run": 0.70, "stretch": 0.20, "g": 9.8}
VARIANTS = [
    {"times": (3.20, 2.95, 2.70, 2.50, 2.30, 2.15, 2.00)},
    {"mass": 8.7},
    {"heights": (22.0, 23.5, 25.0, 26.5, 28.0, 29.5, 31.0)},
]
ANSWER = 0.4961968776737271
TOL = 1e-9
