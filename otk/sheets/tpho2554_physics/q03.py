"""Theory 1.4: the net force mg - kz vanishes at z0 = mgL/(2 B0^2 alpha beta pi^2 R^4) below A. Adapted: the ring's mass, B0 and beta vary; returns z0 in metres for R = 0.50 cm, L = 1.3e-8 H, alpha = 2.0 per metre."""

from math import pi


def solve(mass=50e-6, B0=0.010, alpha=2.0, beta=32.0, radius=0.005, inductance=1.3e-8, g=9.8):
    return mass * g * inductance / (2 * B0**2 * alpha * beta * pi**2 * radius**4)


def check(mass=50e-6, B0=0.010, alpha=2.0, beta=32.0, radius=0.005, inductance=1.3e-8, g=9.8):
    from otk.sheets.tpho2554_physics._ring import lift

    lo, hi = 0.0, 1.0
    while lift(hi, B0, alpha, beta, radius, inductance) < mass * g:
        hi *= 2
    for _ in range(200):
        mid = (lo + hi) / 2
        if lift(mid, B0, alpha, beta, radius, inductance) < mass * g:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"mass": 50e-6, "B0": 0.010, "alpha": 2.0, "beta": 32.0, "radius": 0.005, "inductance": 1.3e-8, "g": 9.8}
VARIANTS = [{"mass": 80e-6}, {"B0": 0.02}, {"beta": 20.0, "mass": 30e-6}]
ANSWER = 0.08067699247521146
TOL = 1e-9
