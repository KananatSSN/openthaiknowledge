"""Theory 3.2 (a)-(d) figure: the moving charges feel qvB upward, as if in E0 = vB; inside the dielectric the field is E1 = E0/epsilon_r, so the polarisation charges (positive on top) add E2 = E1 - E0 = -vB(1 - 1/epsilon_r), pointing down. Adapted: v, B and epsilon_r vary; returns |E2| in V/m."""


def solve(speed=2.0, field=0.5, permittivity=4.0):
    return speed * field * (1 - 1 / permittivity)


def check(speed=2.0, field=0.5, permittivity=4.0):
    # Self-consistent polarisation: the bound-charge field chi E1 opposes
    # E0, E1 = E0 - chi E1; bisect E1, then E2 = E0 - E1 in magnitude.
    from otk.sheets.tpho2557_physics._shared import bisect

    e0 = speed * field
    chi = permittivity - 1
    e1 = bisect(lambda e: e - (e0 - chi * e), 0.0, e0)
    return e0 - e1


PARAMS = {"speed": 2.0, "field": 0.5, "permittivity": 4.0}
VARIANTS = [{"permittivity": 2.5}, {"speed": 5.0, "field": 0.2}, {"permittivity": 10.0}]
ANSWER = 0.75
TOL = 1e-9
