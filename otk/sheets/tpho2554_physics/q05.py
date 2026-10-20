"""Theory 1.6: |I| = B0 alpha pi R^2 z/L grows with depth, so it peaks at the lowest point z = 2 z0, where I_max = mg/(beta pi R^2 B0); 19.5 A for m = 50 mg, R = 0.50 cm, B0 = 0.010 T, beta = 32 per metre. Adapted: mass, R, B0 and beta vary; amperes."""

from math import pi


def solve(mass=50e-6, B0=0.010, beta=32.0, radius=0.005, g=9.8):
    return mass * g / (beta * pi * radius**2 * B0)


def check(mass=50e-6, B0=0.010, beta=32.0, radius=0.005, g=9.8):
    # The peak current does not depend on alpha or L: simulate with the
    # paper's values of both and take the largest |I| on the way down.
    from otk.sheets.tpho2554_physics._ring import current, fall

    alpha, inductance = 2.0, 1.3e-8
    deepest = 0.0
    for _, z, v in fall(mass, B0, alpha, beta, radius, inductance, g=g, dt=1e-5, duration=0.8):
        deepest = max(deepest, z)
    return abs(current(deepest, B0, alpha, radius, inductance))


PARAMS = {"mass": 50e-6, "B0": 0.010, "beta": 32.0, "radius": 0.005, "g": 9.8}
VARIANTS = [{"mass": 80e-6}, {"B0": 0.02, "radius": 0.004}, {"beta": 20.0}]
ANSWER = 19.496480528757182
TOL = 1e-6
