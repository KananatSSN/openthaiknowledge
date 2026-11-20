"""Short9 figure: picture a gives B = mu0 i/(2r), out of the page for counter-clockwise i. In picture b the inner loop (R1) runs counter-clockwise and the outer loop (R2) clockwise, joined by radial leads: B = (mu0 I/2)(1/R1 - 1/R2), out of the page. Returns B / (mu0 I) in m^-1, positive out of the page; radii in cm."""

from math import cos, pi, sin


def solve(inner=2, outer=5, opposed=True):
    sign = -1 if opposed else 1
    return 0.5 * (100 / inner + sign * 100 / outer)


def check(inner=2, outer=5, opposed=True, n=6000):
    # Biot-Savart sum of the z component; counter-clockwise = +.
    def loop(radius, sense):
        total = 0.0
        for k in range(n):
            p = 2 * pi * (k + 0.5) / n
            dl = (-sin(p) * 2 * pi * radius / n * sense, cos(p) * 2 * pi * radius / n * sense)
            r = (-radius * cos(p), -radius * sin(p))
            total += (dl[0] * r[1] - dl[1] * r[0]) / radius**3
        return total / (4 * pi)

    return loop(inner / 100, 1) + loop(outer / 100, -1 if opposed else 1)


PARAMS = {"inner": 2, "outer": 5, "opposed": True}
VARIANTS = [{"opposed": False}, {"inner": 1, "outer": 4}, {"inner": 5, "outer": 10}]
ANSWER = 15.0
