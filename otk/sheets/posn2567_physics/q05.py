"""Short5 figure: two coaxial loops of radius R a small distance d apart carry equal currents I. Each element sees the other loop as a long straight wire d away: per length mu0 I^2/(2 pi d), attractive for parallel currents, times 2 pi R: F ~ mu0 I^2 R / d. Returns the signed force (positive = attraction) in newtons; currents in A, R in cm, d in mm."""

from math import cos, pi, sin, sqrt

MU0 = 4e-7 * pi


def solve(current=10, radius=10, gap=2, same=True):
    force = MU0 * current**2 * (radius / 100) / (gap / 1000)
    return force if same else -force


def check(current=10, radius=10, gap=2, same=True, n=1200):
    # Biot-Savart pairwise: force on loop 2 (z = d) from loop 1 (z = 0),
    # summing dF = I2 dl2 x B1 in the axial direction.
    r, d = radius / 100, gap / 1000
    i2 = current if same else -current
    fz = 0.0
    for a in range(n):
        p = 2 * pi * (a + 0.5) / n
        x2, y2 = r * cos(p), r * sin(p)
        dl2 = (-sin(p) * 2 * pi * r / n, cos(p) * 2 * pi * r / n, 0.0)
        bx = by = bz = 0.0
        for b in range(n):
            q = 2 * pi * (b + 0.5) / n
            x1, y1 = r * cos(q), r * sin(q)
            dl1 = (-sin(q) * 2 * pi * r / n, cos(q) * 2 * pi * r / n, 0.0)
            rx, ry, rz = x2 - x1, y2 - y1, d
            r3 = sqrt(rx * rx + ry * ry + rz * rz) ** 3
            bx += (dl1[1] * rz - dl1[2] * ry) / r3
            by += (dl1[2] * rx - dl1[0] * rz) / r3
            bz += (dl1[0] * ry - dl1[1] * rx) / r3
        scale = MU0 * current / (4 * pi)
        bx, by, bz = bx * scale, by * scale, bz * scale
        fz += i2 * (dl2[0] * by - dl2[1] * bx)
    return -fz  # attraction pulls loop 2 toward loop 1 (negative z)


PARAMS = {"current": 10, "radius": 10, "gap": 2, "same": True}
VARIANTS = [{"same": False}, {"current": 5, "gap": 1}, {"radius": 20}]
TOL = 3e-2
ANSWER = 0.0062831853071795875
