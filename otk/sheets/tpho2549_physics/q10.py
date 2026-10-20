"""Theory 3(c) figure: two electrons in a Thomson atom of charge Q and radius R sit at +-x on a diameter where eQx/(4 pi eps0 R^3) = e^2/(4 pi eps0 (2x)^2), so x = (e/(4Q))^(1/3) R. Adapted: Q = Z e and R given; x in nm."""


def solve(radius=0.2, charge=2):
    return (1 / (4 * charge)) ** (1 / 3) * radius


def check(radius=0.2, charge=2):
    # Bisect the net outward force on one electron (units e^2/(4 pi eps0)).
    def net(x):
        return 1 / (2 * x) ** 2 - charge * x / radius**3

    lo, hi = 1e-9, radius
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if net(mid) > 0 else (lo, mid)
    return lo


PARAMS = {"radius": 0.2, "charge": 2}
VARIANTS = [{"charge": 4}, {"radius": 0.5, "charge": 6}, {"charge": 1}]
ANSWER = 0.1
TOL = 1e-9
