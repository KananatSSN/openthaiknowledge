"""Lab part 3 figures 5-6: by equation (2), sin(theta_c) = 0.508 eta sin(alpha1) + constant, so the slope of sin(theta_c) against eta (least squares) is 0.508 sin(alpha1). Adapted with synthetic fills eta and critical angles (degrees); returns alpha1 in degrees. (The paper's 0.508 is its own linearisation; the exact tangent slope of its x_cm is 16/(3 pi^2) = 0.540.)"""

from math import asin, degrees, radians, sin


def solve(fills=(-0.4, -0.3, -0.2, -0.1, 0.0, 0.1), angles=(6.6, 9.4, 12.3, 15.1, 18.0, 20.9)):
    ys = [sin(radians(a)) for a in angles]
    n = len(fills)
    mx, my = sum(fills) / n, sum(ys) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(fills, ys)) / sum((x - mx) ** 2 for x in fills)
    return degrees(asin(slope / 0.508))


def check(fills=(-0.4, -0.3, -0.2, -0.1, 0.0, 0.1), angles=(6.6, 9.4, 12.3, 15.1, 18.0, 20.9)):
    from otk.sheets.tpho2561_physics._shared import bisect, line

    slope, _ = line(list(fills), [sin(radians(a)) for a in angles])
    return bisect(lambda a: 0.508 * sin(radians(a)) - slope, 0.0, 90.0)


PARAMS = {"fills": (-0.4, -0.3, -0.2, -0.1, 0.0, 0.1), "angles": (6.6, 9.4, 12.3, 15.1, 18.0, 20.9)}
VARIANTS = [{"angles": (5.0, 7.5, 10.0, 12.5, 15.0, 17.5)}, {"angles": (5.0, 6.5, 8.0, 9.5, 11.0, 12.5)}, {"angles": (3.0, 4.5, 6.0, 7.5, 9.0, 10.5)}]
ANSWER = 72.2702776259925
TOL = 1e-9
