"""Theory 1.3: the radial field pushes up on the ring current with |I| 2 pi R B0 beta R, so the net downward force is mg - kz with k = 2 B0^2 alpha beta pi^2 R^4/L. Adapted: B0, alpha, beta and R vary; returns k in N/m for L = 1.3e-8 H."""

from math import pi


def solve(B0=0.010, alpha=2.0, beta=32.0, radius=0.005, inductance=1.3e-8):
    return 2 * B0**2 * alpha * beta * pi**2 * radius**4 / inductance


def check(B0=0.010, alpha=2.0, beta=32.0, radius=0.005, inductance=1.3e-8):
    from otk.sheets.tpho2554_physics._ring import lift

    h, z = 1e-4, 0.03
    up = lift(z + h, B0, alpha, beta, radius, inductance)
    down = lift(z - h, B0, alpha, beta, radius, inductance)
    return (up - down) / (2 * h)


PARAMS = {"B0": 0.010, "alpha": 2.0, "beta": 32.0, "radius": 0.005, "inductance": 1.3e-8}
VARIANTS = [{"beta": 20.0}, {"B0": 0.02, "radius": 0.004}, {"alpha": 3.0}]
ANSWER = 0.006073602708362683
TOL = 1e-9
