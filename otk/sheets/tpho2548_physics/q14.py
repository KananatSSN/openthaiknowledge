"""Theory 3.3: the pressure deficit on the lower disc from a to R pushes it up with F = pi rho K^2 [ln(R/a) - 1/2 + a^2/(2R^2)], K = a^2 v0/(2t). Adapted: numbers; newtons."""

from math import log, pi


def solve(density=1.2, tube=0.01, speed=20, gap=0.002, rim=0.1):
    k = tube**2 * speed / (2 * gap)
    return pi * density * k * k * (log(rim / tube) - 0.5 + tube**2 / (2 * rim**2))


def check(density=1.2, tube=0.01, speed=20, gap=0.002, rim=0.1):
    # Midpoint sum of (P0 - P) 2 pi r dr over rings.
    k = tube**2 * speed / (2 * gap)
    n = 200000
    total = 0.0
    for i in range(n):
        r = tube + (rim - tube) * (i + 0.5) / n
        deficit = density * k * k / 2 * (1 / r**2 - 1 / rim**2)
        total += deficit * 2 * pi * r * (rim - tube) / n
    return total


PARAMS = {"density": 1.2, "tube": 0.01, "speed": 20, "gap": 0.002, "rim": 0.1}
VARIANTS = [{"rim": 0.05}, {"speed": 10, "gap": 0.001}, {"tube": 0.02, "rim": 0.3}]
ANSWER = 1.7036088146665551
TOL = 1e-6
