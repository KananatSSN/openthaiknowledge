"""Theory 2.1 figure 2.1: a rod of length l moving at v across a uniform B (all mutually perpendicular) has V_a - V_b = vBl. Adapted: numbers; volts."""


def solve(speed=4, field=0.5, length=0.2):
    return speed * field * length


def check(speed=4, field=0.5, length=0.2):
    # Inside the rod the electric field balances the magnetic force on the
    # charges, E = vB; integrate it along the rod.
    n = 1000
    return sum(speed * field * length / n for _ in range(n))


PARAMS = {"speed": 4, "field": 0.5, "length": 0.2}
VARIANTS = [{"speed": 10}, {"field": 1.2, "length": 0.05}, {"length": 1.5}]
ANSWER = 0.4
TOL = 1e-9
