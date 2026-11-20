"""Lab 2 item 1: hanging masses stretch the spring by Hooke's law, so k = g/(slope of length against hanging mass), the slope by least squares. Adapted with synthetic readings (grams, cm); returns k in N/m with g = 9.81."""


def solve(masses=(15.5, 31.0, 46.5, 62.0, 77.5), lengths=(21.2, 26.3, 31.5, 36.6, 41.8), g=9.81):
    n = len(masses)
    mx, my = sum(masses) / n, sum(lengths) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(masses, lengths)) / sum((x - mx) ** 2 for x in masses)
    return g / (slope * 1e-2 / 1e-3)


def check(masses=(15.5, 31.0, 46.5, 62.0, 77.5), lengths=(21.2, 26.3, 31.5, 36.6, 41.8), g=9.81):
    # Fit force (N) against length (m) instead: its slope is k itself.
    from otk.sheets.tpho2555_physics._fit import line

    forces = [m * 1e-3 * g for m in masses]
    metres = [x * 1e-2 for x in lengths]
    slope_back, _ = line(forces, metres)
    return 1 / slope_back


PARAMS = {"masses": (15.5, 31.0, 46.5, 62.0, 77.5), "lengths": (21.2, 26.3, 31.5, 36.6, 41.8), "g": 9.81}
VARIANTS = [{"lengths": (20.0, 25.0, 30.0, 35.0, 40.0)}, {"masses": (10.0, 20.0, 30.0, 40.0, 50.0)}, {"lengths": (30.1, 33.0, 36.2, 39.1, 42.0)}]
ANSWER = 2.95252427184466
TOL = 1e-9
