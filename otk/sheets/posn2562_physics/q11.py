"""MC11 figure: inner and outer semicircular arcs centeredO radiiR1<R2 connected by straight RADIAL segments on diameter. Outer currentcounterclockwise, innerclockwise, fieldsoppose; radialfields0. |B|/(mu I)=(1/R1-1/R2)/4, source answer1."""

from math import pi, cos, sin


def solve(inner=1, outer=2):
    return (1 / inner - 1 / outer) / 4


def check(inner=1, outer=2):
    # Biot-Savart midpoint quadrature: dl cross (O-r)/|O-r|^3.
    steps = 1000
    total = 0.0
    for radius, direction in ((outer, 1), (inner, -1)):
        dphi = pi / steps
        for i in range(steps):
            phi = (i + 0.5) * dphi
            x, y = radius * cos(phi), radius * sin(phi)
            dlx, dly = -direction * y * dphi, direction * x * dphi
            total += (dlx * (-y) - dly * (-x)) / (4 * pi * (x * x + y * y) ** 1.5)
    return abs(total)


PARAMS = {"inner": 1, "outer": 2}
VARIANTS = [{"inner": 0.5}, {"outer": 3}, {"inner": 2, "outer": 5}]
ANSWER = 0.125
