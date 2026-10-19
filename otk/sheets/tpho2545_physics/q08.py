"""Theory II.b: rolling on the rod, the hoop spins at (1 - r/R) theta' and its centre moves at (R - r) theta'; KE = (1/2) M R^2 (1 - r/R)^2 theta'^2 + (1/2) M (R - r)^2 theta'^2 = M (R - r)^2 theta'^2. Joules."""


def solve(mass=2, hoop=0.5, rod=0.1, rate=3):
    return mass * (hoop - rod) ** 2 * rate**2


def check(mass=2, hoop=0.5, rod=0.1, rate=3, n=20000):
    # Sum (1/2) dm v^2 over the hoop: each point moves with the centre's
    # velocity plus spin; the instantaneous pivot is the contact point, so
    # v = spin * distance to contact, with spin (R - r) theta' / R.
    from math import cos, pi, sin

    spin = (hoop - rod) * rate / hoop
    total = 0.0
    for k in range(n):
        p = 2 * pi * (k + 0.5) / n
        # contact at the top of the hoop: (0, R) relative to the centre
        dx, dy = hoop * cos(p), hoop * sin(p) - hoop
        total += 0.5 * mass / n * spin * spin * (dx * dx + dy * dy)
    return total


PARAMS = {"mass": 2, "hoop": 0.5, "rod": 0.1, "rate": 3}
VARIANTS = [{"rod": 0.0}, {"mass": 1, "hoop": 1.0, "rod": 0.5}, {"rate": 0.5}]
TOL = 1e-6
ANSWER = 2.880000000000001
