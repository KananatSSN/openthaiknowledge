"""Lab part 2: at terminal speed mg = k s/t, so t = (k s/g)(1/m) and k = g (slope)/s; the solution's slope 27.05 g s over a 1.01 m tube gives k = 0.262 kg/s (it prints 0.265). Adapted with synthetic masses (g) and fall times (s) over the tube length (m); returns k in kg/s with g = 9.78."""


def solve(masses=(7.60, 9.48, 11.36, 13.24, 15.12, 17.00), times=(3.82, 3.06, 2.65, 2.38, 2.07, 1.84), tube=1.01, g=9.78):
    xs = [1 / m for m in masses]
    n = len(xs)
    mx, my = sum(xs) / n, sum(times) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, times)) / sum((x - mx) ** 2 for x in xs)
    return slope * 1e-3 * g / tube


def check(masses=(7.60, 9.48, 11.36, 13.24, 15.12, 17.00), times=(3.82, 3.06, 2.65, 2.38, 2.07, 1.84), tube=1.01, g=9.78):
    # Fit in SI units (kg, s) by Cramer's rule.
    from otk.sheets.tpho2560_physics._shared import line

    slope, _ = line([1 / (m * 1e-3) for m in masses], list(times))
    return slope * g / tube


PARAMS = {"masses": (7.60, 9.48, 11.36, 13.24, 15.12, 17.00), "times": (3.82, 3.06, 2.65, 2.38, 2.07, 1.84), "tube": 1.01, "g": 9.78}
VARIANTS = [{"tube": 1.20}, {"times": (4.10, 3.30, 2.80, 2.45, 2.15, 1.95)}, {"times": (3.40, 2.75, 2.30, 2.00, 1.75, 1.60), "tube": 0.90}]
ANSWER = 0.2567489952027476
TOL = 1e-9
