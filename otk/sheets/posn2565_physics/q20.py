"""MC20 figure: infinite wires along OX and OY each carry I (both through O). At (0,0,z) each gives mu0 I/(2 pi z) and the two fields are perpendicular, so B = mu0 I/(sqrt2 pi z) (answer 3). Adapted: currents I1, I2; returns B in microtesla for z in m."""

from math import sqrt

MU0_OVER_2PI = 2e-7


def solve(along_x=3, along_y=4, height=0.5):
    return MU0_OVER_2PI * sqrt(along_x**2 + along_y**2) / height * 1e6


def check(along_x=3, along_y=4, height=0.5):
    # Biot-Savart along both wires from -L to L, summed as vectors.
    def wire(current, direction, n=200000, span=2000.0):
        bx = by = bz = 0.0
        h = 2 * span / n
        for k in range(n):
            s = -span + (k + 0.5) * h
            pos = (s, 0.0, 0.0) if direction == "x" else (0.0, s, 0.0)
            dl = (h, 0.0, 0.0) if direction == "x" else (0.0, h, 0.0)
            r = (-pos[0], -pos[1], height)
            r3 = (r[0] ** 2 + r[1] ** 2 + r[2] ** 2) ** 1.5
            bx += current * (dl[1] * r[2] - dl[2] * r[1]) / r3
            by += current * (dl[2] * r[0] - dl[0] * r[2]) / r3
            bz += current * (dl[0] * r[1] - dl[1] * r[0]) / r3
        return bx, by, bz

    a, b = wire(along_x, "x"), wire(along_y, "y")
    total = sqrt(sum((p + q) ** 2 for p, q in zip(a, b)))
    return 1e-7 * total * 1e6


PARAMS = {"along_x": 3, "along_y": 4, "height": 0.5}
VARIANTS = [{"along_x": 5, "along_y": 12, "height": 2}, {"along_x": 1, "along_y": 1}, {"height": 0.2}]
TOL = 1e-4
ANSWER = 2.0
