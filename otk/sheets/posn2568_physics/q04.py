"""Short4 figure: ring of radius R in the XOY plane carries +Q; at (0,0,-L) the field is k Q L/(R^2 + L^2)^(3/2) along -Z. Returns E_z in V/m (negative = along -Z) for Q in nC and lengths in m, k = 9e9."""

from math import cos, pi, sin

K = 9e9


def solve(charge=5, radius=3, distance=4):
    return -K * charge * 1e-9 * distance / (radius**2 + distance**2) ** 1.5


def check(charge=5, radius=3, distance=4, n=4000):
    # Coulomb sum over ring elements at the point (0, 0, -L).
    q = charge * 1e-9 / n
    ex = ey = ez = 0.0
    for k in range(n):
        p = 2 * pi * (k + 0.5) / n
        dx, dy, dz = -radius * cos(p), -radius * sin(p), -distance
        r3 = (dx * dx + dy * dy + dz * dz) ** 1.5
        ex += K * q * dx / r3
        ey += K * q * dy / r3
        ez += K * q * dz / r3
    assert abs(ex) < 1e-6 and abs(ey) < 1e-6
    return ez


PARAMS = {"charge": 5, "radius": 3, "distance": 4}
VARIANTS = [{"radius": 5, "distance": 12}, {"charge": 1, "radius": 8, "distance": 6}, {"distance": 1}]
ANSWER = -1.44
