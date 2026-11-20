"""MC8 figure: ring radius R with charge q spread evenly; Q on the ring's axis at distance x from the centre. F = (qQ/4 pi eps0) x / (x^2 + R^2)^(3/2) (answer 3). Returns F / (k q Q) in m^-2."""

from math import cos, sin, pi


def solve(radius=3, distance=4):
    return distance / (distance**2 + radius**2) ** 1.5


def check(radius=3, distance=4):
    # Sum Coulomb vectors from 4000 ring elements; the transverse parts cancel.
    n = 4000
    fx = fy = fz = 0.0
    for k in range(n):
        phi = 2 * pi * k / n
        dx, dy, dz = distance, -radius * cos(phi), -radius * sin(phi)
        r3 = (dx * dx + dy * dy + dz * dz) ** 1.5
        fx += dx / r3 / n
        fy += dy / r3 / n
        fz += dz / r3 / n
    assert abs(fy) < 1e-9 and abs(fz) < 1e-9
    return fx


PARAMS = {"radius": 3, "distance": 4}
VARIANTS = [{"radius": 5, "distance": 12}, {"radius": 8, "distance": 6}, {"radius": 1, "distance": 1}]
ANSWER = 0.032
