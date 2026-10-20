"""Theory 1 g): with phi = theta - pi/2 the motion obeys phi_dot = beta sqrt(sin phi), beta = sqrt(p q0/(2 pi eps0 m0 r0^4)), so the charge returns after T = (4/beta) integral_0^(pi/2) dphi/sqrt(sin phi) ~ (4/beta)(2 sqrt(pi/2) + (pi/2)^(5/2)/30) = 10.44/beta using the paper's approximation (the solution writes 10.3/beta; the exact integral gives 10.49/beta). Adapted: the dipole moment (nC m), q0 (uC), m0 (g) and r0 (cm) vary; returns seconds."""

from math import pi, sqrt


def solve(moment=1.0, charge=1.0, mass=1.0, radius=5.0):
    from otk.sheets.tpho2565_physics._shared import EPS0

    beta = sqrt(moment * 1e-9 * charge * 1e-6 / (2 * pi * EPS0 * mass * 1e-3 * (radius * 1e-2) ** 4))
    return 4 / beta * (2 * sqrt(pi / 2) + sqrt((pi / 2) ** 5) / 30)


def check(moment=1.0, charge=1.0, mass=1.0, radius=5.0, steps=20000):
    from math import sin

    from otk.sheets.tpho2565_physics._shared import EPS0

    # the exact quarter-swing integral, with phi = u^2 to remove the endpoint singularity
    beta = sqrt(moment * 1e-9 * charge * 1e-6 / (2 * pi * EPS0 * mass * 1e-3 * (radius * 1e-2) ** 4))
    top = sqrt(pi / 2)
    du = top / steps
    quarter = sum(2 * u / sqrt(sin(u * u)) * du for u in ((i + 0.5) * du for i in range(steps)))
    return 4 / beta * quarter


PARAMS = {"moment": 1.0, "charge": 1.0, "mass": 1.0, "radius": 5.0}
VARIANTS = [{"radius": 10.0}, {"mass": 4.0}, {"moment": 2.0}]
ANSWER = 0.1946488376617204
TOL = 1e-2
