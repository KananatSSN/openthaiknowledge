"""MC17 figure: coaxial cylinders of length l, radii r and r + d with d small; like a parallel plate of area 2 pi r l, C = 2 pi eps0 r l / d (answer 2). Returns C / eps0 in metres for r, l in cm and d in mm."""

from math import log, pi


def solve(radius=5, length=20, gap=1):
    return 2 * pi * (radius / 100) * (length / 100) / (gap / 1000)


def check(radius=5, length=20, gap=1):
    # Exact coaxial formula 2 pi l / ln(1 + d/r); the thin-gap limit is the
    # leading term, so compare after removing the first correction (1 + d/2r); the
    # remaining relative error is about (d/r)^2/12.
    r, span, d = radius / 100, length / 100, gap / 1000
    exact = 2 * pi * span / log(1 + d / r)
    return exact / (1 + d / (2 * r))


PARAMS = {"radius": 5, "length": 20, "gap": 1}
VARIANTS = [{"radius": 10, "gap": 2}, {"length": 50}, {"radius": 2, "length": 10, "gap": 0.5}]
TOL = 1e-4
ANSWER = 62.83185307179587
