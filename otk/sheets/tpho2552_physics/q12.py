"""Theory 3.4: the plate cannot oscillate once omega^2 <= 0, i.e. k <= V0^2 A eps0/(D - d)^3 = 2kd/(D - d): d >= D/3. Adapted: D given; returns the least such stretch d in the same unit."""


def solve(gap=12.0):
    return gap / 3


def check(gap=12.0):
    # Bisect on d for the sign change of omega^2 = (k/m)(D - 3d)/(D - d).
    lo, hi = 0.0, gap * 0.999
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if (gap - 3 * mid) / (gap - mid) > 0 else (lo, mid)
    return hi


PARAMS = {"gap": 12.0}
VARIANTS = [{"gap": 9.0}, {"gap": 4.5}, {"gap": 30.0}]
ANSWER = 4.0
TOL = 1e-9
