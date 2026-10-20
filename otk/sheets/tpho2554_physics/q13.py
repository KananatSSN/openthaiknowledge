"""Theory 3.2 figure 2: cut a short water cylinder of radius R and height h along a diameter; P 2Rh = P0 2Rh + 2 gamma h, so the water pressure exceeds the air's by gamma/R. Adapted: gamma and R (mm) vary; pascals."""


def solve(tension=0.072, radius=1.0):
    return tension / (radius * 1e-3)


def check(tension=0.072, radius=1.0):
    # Integrate the pressure excess's push across the cut over the half
    # circumference (midpoint rule) and balance the two surface-tension lines.
    from math import pi, sin

    R = radius * 1e-3
    n = 2000
    push = sum(sin((i + 0.5) * pi / n) for i in range(n)) * pi / n * R   # per unit excess and height
    return 2 * tension / push


PARAMS = {"tension": 0.072, "radius": 1.0}
VARIANTS = [{"radius": 1.33}, {"tension": 0.05, "radius": 0.5}, {"radius": 3.0}]
ANSWER = 72.0
TOL = 1e-6
