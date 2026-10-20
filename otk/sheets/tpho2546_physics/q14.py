"""Theory 3.5 figure (b): a charge -q' at P, r0 from the centre; Q is on the far side, r from the centre: V_Q = (rho/2 eps0)(R^2 - r^2/3) - q'/(4 pi eps0 (r0 + r)). Adapted: q' equals the charge of a ball of radius s at density rho, so V_Q = (rho/eps0)[(3R^2 - r^2)/6 - s^3/(3(r0 + r))]; returns V_Q in units of rho/eps0."""

from math import pi, sqrt


def solve(radius=1.0, point=0.4, source=0.3, size=0.5):
    return (3 * radius**2 - point**2) / 6 - size**3 / (3 * (source + point))


def check(radius=1.0, point=0.4, source=0.3, size=0.5):
    # Ball: field integrated inward from infinity; point charge: Coulomb at
    # the distance between P (x = -r0) and Q (x = r), from coordinates.
    charge = 4 / 3 * pi * radius**3
    n = 4000
    ball = sum(charge / (4 * pi * (radius / ((k + 0.5) / n)) ** 2) * radius / ((k + 0.5) / n) ** 2 / n for k in range(n))
    ball += sum((point + (radius - point) * (k + 0.5) / n) / 3 * (radius - point) / n for k in range(n))
    p, q = (-source, 0.0), (point, 0.0)
    distance = sqrt((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)
    return ball - (4 / 3 * pi * size**3) / (4 * pi * distance)


PARAMS = {"radius": 1.0, "point": 0.4, "source": 0.3, "size": 0.5}
VARIANTS = [{"point": 0.0}, {"source": 0.8, "size": 0.2}, {"radius": 2.0, "point": 1.5, "source": 1.0}]
ANSWER = 0.4138095238095238
TOL = 1e-6
