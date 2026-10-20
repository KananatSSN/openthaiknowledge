"""Theory 3.2 figure: the upper plate (mass m) hangs on a conducting spring k, D above the fixed lower plate when V = 0; at V = V0 the spring stretches by d more, so k d = (1/2) eps0 A (V0/(D - d))^2 and k = (V0/(D - d))^2 A eps0/(2d). Adapted: numbers vary; N/m."""

EPS0 = 8.85e-12


def solve(volts=1000.0, area=0.05, gap=0.01, stretch=0.002):
    field = volts / (gap - stretch)
    return field**2 * area * EPS0 / (2 * stretch)


def check(volts=1000.0, area=0.05, gap=0.01, stretch=0.002):
    # Bisect on k: the plate's stable equilibrium stretch for that k (on the
    # branch below D/3) must be d.
    def stretch_for(k):
        lo, hi = 0.0, gap / 3
        for _ in range(200):
            mid = (lo + hi) / 2
            force = 0.5 * EPS0 * area * (volts / (gap - mid)) ** 2 - k * mid
            lo, hi = (mid, hi) if force > 0 else (lo, mid)
        return lo

    lo, hi = 1e-6, 1e6
    for _ in range(200):
        mid = (lo * hi) ** 0.5
        lo, hi = (lo, mid) if stretch_for(mid) < stretch else (mid, hi)
    return lo


PARAMS = {"volts": 1000.0, "area": 0.05, "gap": 0.01, "stretch": 0.002}
VARIANTS = [{"volts": 500.0}, {"area": 0.2, "stretch": 0.001}, {"gap": 0.02, "stretch": 0.005}]
ANSWER = 1.728515625
TOL = 1e-4
