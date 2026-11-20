"""Theory 2 (e): dE/E = y d(omega)/omega with dE/E0 = d(omega)/omega0 gives y = 1, so E = E0 omega/omega0 and at omega1 the energy is E0 omega1/omega0. Adapted: E0 (mJ), omega0 and omega1 vary; returns the energy in mJ."""


def solve(energy=40.0, omega=10.0, later=8.0):
    return energy * later / omega


def check(energy=40.0, omega=10.0, later=8.0):
    # Add dust in many tiny portions: each cycle loses dE = E dm/(2m) and
    # the frequency follows omega = sqrt(k/m).
    from math import sqrt

    mass, k = 1.0, omega**2
    E = energy
    target = k / later**2
    steps = 200000
    dm = (target - mass) / steps
    for _ in range(steps):
        E -= E * dm / (2 * mass)
        mass += dm
    assert abs(sqrt(k / mass) - later) < 1e-9
    return E


PARAMS = {"energy": 40.0, "omega": 10.0, "later": 8.0}
VARIANTS = [{"later": 5.0}, {"energy": 100.0, "omega": 20.0, "later": 15.0}, {"later": 9.5}]
ANSWER = 32.0
TOL = 1e-4
