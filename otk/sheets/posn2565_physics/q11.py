"""MC11 figure: picture b joins a half circle of radius R1 and a half circle of radius R2 about O, current circulating the same way in both, by radial leads. B_O = (mu0 I / 4)(1/R1 + 1/R2) = (B R / 2)(1/R1 + 1/R2) with B = mu0 I/(2R) (answer 1). Returns B_O / (mu0 I) in m^-1 for radii in cm."""

from math import cos, sin, pi


def solve(inner=2, outer=5):
    return 0.25 * (100 / inner + 100 / outer)


def check(inner=2, outer=5):
    # Biot-Savart sum over both half circles (upper on R1, lower on R2, both
    # counter-clockwise), in units mu0 I / (4 pi) -> divide by 4 pi at the end.
    def arc(radius, start, n=4000):
        total = 0.0
        for k in range(n):
            phi = start + pi * (k + 0.5) / n
            dl = (-sin(phi) * radius * pi / n, cos(phi) * radius * pi / n)
            r = (-radius * cos(phi), -radius * sin(phi))
            total += (dl[0] * r[1] - dl[1] * r[0]) / radius**3
        return total

    total = arc(inner / 100, 0.0) + arc(outer / 100, pi)
    return total / (4 * pi)


PARAMS = {"inner": 2, "outer": 5}
VARIANTS = [{"inner": 1, "outer": 4}, {"inner": 5, "outer": 10}, {"inner": 3, "outer": 4}]
ANSWER = 17.5
