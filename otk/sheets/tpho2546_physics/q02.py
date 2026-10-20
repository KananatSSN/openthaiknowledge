"""Theory 1.1 figure: the same quarter cylinder; its speed V = m v cos theta/(M + m), from zero horizontal momentum m(v cos theta - V) = MV. Adapted: numbers for M, m, R, theta; m/s."""

from math import cos, radians, sin, sqrt


def solve(big=4, small=1, radius=0.5, angle=60, g=10):
    c, s = cos(radians(angle)), sin(radians(angle))
    v = sqrt(2 * g * radius * (big + small) * (1 - c) / (big + small * s * s))
    return small * v * c / (big + small)


def check(big=4, small=1, radius=0.5, angle=60, g=10):
    # Ground frame, unknowns (V, w = d theta/dt): zero momentum and energy,
    # solved by Newton iteration from a rough guess.
    c, s = cos(radians(angle)), sin(radians(angle))

    def equations(V, w):
        ux, uy = radius * w * c - V, -radius * w * s
        momentum = small * ux - big * V
        energy = 0.5 * small * (ux * ux + uy * uy) + 0.5 * big * V * V - small * g * radius * (1 - c)
        return momentum, energy

    V, w = 0.1, 1.0
    for _ in range(100):
        f1, f2 = equations(V, w)
        h = 1e-7
        a11 = (equations(V + h, w)[0] - f1) / h
        a12 = (equations(V, w + h)[0] - f1) / h
        a21 = (equations(V + h, w)[1] - f2) / h
        a22 = (equations(V, w + h)[1] - f2) / h
        det = a11 * a22 - a12 * a21
        V, w = V - (f1 * a22 - f2 * a12) / det, w - (a11 * f2 - a21 * f1) / det
    return V


PARAMS = {"big": 4, "small": 1, "radius": 0.5, "angle": 60, "g": 10}
VARIANTS = [{"big": 1, "small": 1}, {"angle": 30, "radius": 1.2}, {"big": 10, "small": 3, "angle": 45}]
ANSWER = 0.2294157338705618
TOL = 1e-6
