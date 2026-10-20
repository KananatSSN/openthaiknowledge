"""Lab 1, parts 1.2 and 1.4: 1/V_C^2 = 2/E0^2 + (2 w^2 C^2/E0^2) R^2 is a line in R^2, so C = sqrt(slope/intercept)/w. Adapted: synthetic slope (V^-2 ohm^-2) and intercept (V^-2) at f = 50 Hz; farads."""

from math import pi, sqrt


def solve(slope=2e-9, intercept=0.02, omega=100 * pi):
    return sqrt(slope / intercept) / omega


def check(slope=2e-9, intercept=0.02, omega=100 * pi):
    # Recover E0 from the intercept, then bisect on C until the circuit's
    # 1/V_C^2 at two resistances reproduces the slope.
    amplitude = sqrt(2 / intercept)

    def inverse_square(r, c):
        zc = 1 / (1j * omega * c)
        v = abs(amplitude * zc / (r + zc)) / sqrt(2)
        return 1 / (v * v)

    def fitted_slope(c):
        return (inverse_square(3300, c) - inverse_square(680, c)) / (3300**2 - 680**2)

    lo, hi = 1e-12, 1.0
    for _ in range(200):
        mid = sqrt(lo * hi)
        lo, hi = (mid, hi) if fitted_slope(mid) < slope else (lo, mid)
    return lo


PARAMS = {"slope": 2e-9, "intercept": 0.02, "omega": 100 * pi}
VARIANTS = [{"slope": 8e-9}, {"intercept": 0.08, "slope": 1e-9}, {"omega": 1000}]
ANSWER = 1.0065842420897406e-06
TOL = 1e-7
