"""Lab part 1: each wheel (radius R on an axle of radius R0) is a Faraday disc with emf B w (R^2 - R0^2)/2, w = v/R; two wheels in series give V = vB(R^2 - R0^2)/R, and with v^2 = 2as, V^2 = 2 a s B^2 ((R^2 - R0^2)/R)^2, a straight line in a = 2s/t^2. The solution's slope 9.33e-6 V^2 s^2/m gives B = 0.294 T. Adapted with synthetic times (s) and voltages (mV) over s = 70 cm, R = 9.50 mm, R0 = 2.60 mm; returns B in tesla."""

from math import sqrt


def solve(times=(2.50, 2.06, 1.73, 1.56, 1.39, 1.29, 1.20), volts=(1.53, 1.67, 1.97, 2.27, 2.57, 2.76, 3.03), run=0.70, wheel=9.50, axle=2.60):
    xs = [2 * run / t**2 for t in times]
    ys = [(v * 1e-3) ** 2 for v in volts]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    R, R0 = wheel * 1e-3, axle * 1e-3
    return sqrt(slope / (2 * run * ((R * R - R0 * R0) / R) ** 2))


def check(times=(2.50, 2.06, 1.73, 1.56, 1.39, 1.29, 1.20), volts=(1.53, 1.67, 1.97, 2.27, 2.57, 2.76, 3.03), run=0.70, wheel=9.50, axle=2.60):
    # Fit by Cramer's rule, then integrate the Faraday-disc emf over the
    # disc's annulus numerically instead of using the closed form.
    from otk.sheets.tpho2557_physics._shared import line

    slope, _ = line([2 * run / t**2 for t in times], [(v * 1e-3) ** 2 for v in volts])
    R, R0 = wheel * 1e-3, axle * 1e-3
    n = 10000
    # emf of both wheels per unit B per unit speed: 2 * integral (r/R) dr from R0 to R
    per = 2 * sum(((R0 + (i + 0.5) * (R - R0) / n) / R) * (R - R0) / n for i in range(n))
    return sqrt(slope / (2 * run * per**2))


PARAMS = {"times": (2.50, 2.06, 1.73, 1.56, 1.39, 1.29, 1.20), "volts": (1.53, 1.67, 1.97, 2.27, 2.57, 2.76, 3.03), "run": 0.70, "wheel": 9.50, "axle": 2.60}
VARIANTS = [
    {"volts": (1.80, 2.05, 2.40, 2.70, 3.10, 3.35, 3.65)},
    {"times": (2.40, 2.00, 1.70, 1.50, 1.35, 1.25, 1.15)},
    {"volts": (1.0, 1.2, 1.4, 1.6, 1.8, 1.95, 2.1)},
]
ANSWER = 0.2940688135454567
TOL = 1e-9
