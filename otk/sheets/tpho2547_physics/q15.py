"""Lab 2, parts 2.3 and 2.4: (V_L/V_R)^2 = ((omega L)^2 + r^2)/R^2 is a line through the origin in 1/R^2 whose slope gives L = sqrt(slope - r^2)/omega. Adapted: a synthetic slope (ohm^2) with r = 38 ohm and f = 50 Hz; henries."""

from math import pi, sqrt


def solve(slope=1444 + 300**2, coil=38, omega=100 * pi):
    return sqrt(slope - coil**2) / omega


def check(slope=1444 + 300**2, coil=38, omega=100 * pi):
    # Bisect on L until the circuit's (V_L/V_R)^2 at two resistances gives the
    # stated slope against 1/R^2.
    def ratio_squared(r, inductance):
        z = complex(coil, omega * inductance)
        return abs(z) ** 2 / r**2

    def fitted(inductance):
        return (ratio_squared(560, inductance) - ratio_squared(2000, inductance)) / (1 / 560**2 - 1 / 2000**2)

    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if fitted(mid) < slope else (lo, mid)
    return lo


PARAMS = {"slope": 1444 + 300**2, "coil": 38, "omega": 100 * pi}
VARIANTS = [{"slope": 1444 + 100**2}, {"coil": 0, "slope": 250000}, {"omega": 1000, "slope": 1444 + 500**2}]
ANSWER = 0.954929658551372
TOL = 1e-6
