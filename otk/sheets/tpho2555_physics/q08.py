"""Theory 2 (d): omega^2 = k/m gives 2 d(omega)/omega0 = -dm/m, and dE = -dm E0/(2m), so d(omega)/omega0 = dE/E0. Adapted: omega0, E0 (mJ) and the energy lost (microjoules) vary; returns the drop in omega (rad/s)."""


def solve(omega=10.0, energy=40.0, loss=5.0):
    return omega * loss * 1e-6 / (energy * 1e-3)


def check(omega=10.0, energy=40.0, loss=5.0):
    # The dust that removes this energy, dm = 2 m dE/E0, put on exactly
    # (scaled down and back up to stay first order).
    from math import sqrt

    mass = 1.0
    k = omega**2 * mass
    scale = 1e-4
    dm = 2 * mass * loss * 1e-6 / (energy * 1e-3) * scale
    return (omega - sqrt(k / (mass + dm))) / scale


PARAMS = {"omega": 10.0, "energy": 40.0, "loss": 5.0}
VARIANTS = [{"omega": 25.0}, {"energy": 100.0}, {"loss": 20.0}]
ANSWER = 0.0012499999999999998
TOL = 1e-6
