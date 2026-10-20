"""Lab part 1: the horizontal jet falls y in t = sqrt(2y/g) and lands x = ut away, so Q = pi r^2 u = (sqrt(g/(2y)) pi r^2) x and the slope of Q against x gives r^2 = slope sqrt(2y/g)/pi; 0.0518 cm^2/s at y = 5.9 cm gives r = 0.425 mm. Adapted with synthetic ranges x (cm) and flows Q (ml/s); returns r in mm with g = 9.8."""

from math import pi, sqrt


def solve(ranges=(7.4, 8.6, 9.8, 11.4, 12.1, 13.5), flows=(0.44, 0.51, 0.56, 0.62, 0.68, 0.77), height=5.9, g=9.8):
    n = len(ranges)
    mx, my = sum(ranges) / n, sum(flows) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(ranges, flows)) / sum((x - mx) ** 2 for x in ranges)
    slope_si = slope * 1e-6 / 1e-2             # (ml/s)/cm -> m^2/s
    return sqrt(slope_si * sqrt(2 * height * 1e-2 / g) / pi) * 1e3


def check(ranges=(7.4, 8.6, 9.8, 11.4, 12.1, 13.5), flows=(0.44, 0.51, 0.56, 0.62, 0.68, 0.77), height=5.9, g=9.8):
    # Fit by Cramer's rule, then bisect the radius whose predicted slope matches.
    from otk.sheets.tpho2558_physics._shared import bisect, line

    slope, _ = line([x * 1e-2 for x in ranges], [q * 1e-6 for q in flows])
    return bisect(lambda r: sqrt(g / (2 * height * 1e-2)) * pi * r * r - slope, 0.0, 1e-2) * 1e3


PARAMS = {"ranges": (7.4, 8.6, 9.8, 11.4, 12.1, 13.5), "flows": (0.44, 0.51, 0.56, 0.62, 0.68, 0.77), "height": 5.9, "g": 9.8}
VARIANTS = [{"height": 8.0}, {"flows": (0.40, 0.46, 0.52, 0.60, 0.64, 0.71)}, {"ranges": (6.0, 7.5, 9.0, 10.5, 12.0, 13.5)}]
ANSWER = 0.42531555103441193
TOL = 1e-9
