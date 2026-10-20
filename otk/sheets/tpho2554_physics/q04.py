"""Theory 1.5: about z0 the ring obeys m s'' + k s = 0, so it oscillates with omega = sqrt(2 B0^2 alpha beta pi^2 R^4/(mL)) and amplitude z0. Adapted: mass, B0 and beta vary; returns omega in rad/s for R = 0.50 cm, L = 1.3e-8 H, alpha = 2.0 per metre."""

from math import pi, sqrt


def solve(mass=50e-6, B0=0.010, alpha=2.0, beta=32.0, radius=0.005, inductance=1.3e-8):
    return sqrt(2 * B0**2 * alpha * beta * pi**2 * radius**4 / (mass * inductance))


def check(mass=50e-6, B0=0.010, alpha=2.0, beta=32.0, radius=0.005, inductance=1.3e-8):
    # Release the ring from A and time two successive lowest points.
    from otk.sheets.tpho2554_physics._ring import fall

    turns, last = [], None
    for t, _, v in fall(mass, B0, alpha, beta, radius, inductance, duration=4.0):
        if last is not None and last[1] > 0 >= v:
            t0, v0 = last
            turns.append(t0 + (t - t0) * v0 / (v0 - v))
            if len(turns) == 2:
                return 2 * pi / (turns[1] - turns[0])
        last = (t, v)
    raise ValueError("fewer than two turning points")


PARAMS = {"mass": 50e-6, "B0": 0.010, "alpha": 2.0, "beta": 32.0, "radius": 0.005, "inductance": 1.3e-8}
VARIANTS = [{"mass": 80e-6}, {"B0": 0.02}, {"beta": 20.0}]
ANSWER = 11.021436120907913
TOL = 1e-6
