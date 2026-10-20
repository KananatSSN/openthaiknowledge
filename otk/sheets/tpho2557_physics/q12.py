"""Theory 3.2 (e): only the polarisation field E2 = vB(1 - 1/epsilon_r) drives charge round the circuit, so the plates see emf = vBd(1 - 1/epsilon_r). Adapted: v, B, d (mm) and epsilon_r vary; returns the emf in mV."""


def solve(speed=2.0, field=0.5, gap=2.0, permittivity=4.0):
    return speed * field * gap * 1e-3 * (1 - 1 / permittivity) * 1e3


def check(speed=2.0, field=0.5, gap=2.0, permittivity=4.0):
    # Integrate the polarisation field across the gap (midpoint rule).
    e2 = speed * field - speed * field / permittivity
    n = 1000
    return sum(e2 * gap * 1e-3 / n for _ in range(n)) * 1e3


PARAMS = {"speed": 2.0, "field": 0.5, "gap": 2.0, "permittivity": 4.0}
VARIANTS = [{"permittivity": 2.5}, {"gap": 5.0}, {"speed": 0.5, "field": 1.2}]
ANSWER = 1.5
TOL = 1e-9
