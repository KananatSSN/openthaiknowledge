"""Theory 2.2: heating 1 mol slowly by dT keeps P0 fixed, so dV = R dT/P0 and the pistons rise S = R dT/(Pa (A - a) + Mg). Adapted: numbers; metres with R = 8.31, g = 9.8."""


def solve(outside=1.0e5, mass=20, big=0.05, small=0.01, warming=30, gas=8.31, g=9.8):
    return gas * warming / (outside * (big - small) + mass * g)


def check(outside=1.0e5, mass=20, big=0.05, small=0.01, warming=30, gas=8.31, g=9.8, start=300):
    # Ideal-gas volumes before and after at the equilibrium pressure, then
    # the piston travel that makes that volume change.
    pressure = outside + mass * g / (big - small)
    before = gas * start / pressure
    after = gas * (start + warming) / pressure
    return (after - before) / (big - small)


PARAMS = {"outside": 1.0e5, "mass": 20, "big": 0.05, "small": 0.01, "warming": 30, "gas": 8.31, "g": 9.8}
VARIANTS = [{"warming": 5}, {"mass": 5, "big": 0.03}, {"outside": 9.0e4}]
ANSWER = 0.0594137273593899
TOL = 1e-9
