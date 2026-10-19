"""Short25 figure: semi-infinite wires ab and ed (current I, opposite ways) end on the line through O at distance R either side, joined by a semicircle bcd of radius R about O; all three parts circulate one way. B = mu0 I/(4R) + 2 mu0 I/(4 pi R) = (mu0 I/(4R))(1 + 2/pi). Returns B / (mu0 I) in m^-1 for R in cm."""

from math import cos, pi, sin


def solve(radius=5):
    r = radius / 100
    return (1 + 2 / pi) / (4 * r)


def check(radius=5, n=200000, span=200.0):
    # Biot-Savart sum (units mu0 I = 1) of the z component over the path:
    # e -> d along y = -r from x = -span to 0, the semicircle d -> c -> b on
    # the right (x > 0), then b -> a along y = +r back to x = -span.
    r = radius / 100
    total = 0.0
    h = span / n
    for k in range(n):
        x = -span + (k + 0.5) * h
        # bottom wire, dl = (+h, 0), from (x, -r) to O
        total += (h * r) / (x * x + r * r) ** 1.5
        # top wire, dl = (-h, 0), at (x, +r)
        total += (h * r) / (x * x + r * r) ** 1.5
    m = 20000
    for k in range(m):
        p = -pi / 2 + pi * (k + 0.5) / m
        dl = (-sin(p) * pi * r / m, cos(p) * pi * r / m)
        rel = (-r * cos(p), -r * sin(p))
        total += (dl[0] * rel[1] - dl[1] * rel[0]) / r**3
    return total / (4 * pi)


PARAMS = {"radius": 5}
VARIANTS = [{"radius": 2}, {"radius": 10}, {"radius": 1}]
TOL = 1e-4
ANSWER = 8.183098861837907
