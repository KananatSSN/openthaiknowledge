"""Theory 1.2.2 figure: the lowest temperature is at C, directly below A at the same volume, so p_C = p_A T_min/T_A = 10 atm (300/400) = 7.5 atm. Adapted: p_A (atm), T_A and T_min (K) vary; returns p_C in atm."""


def solve(pressure=10.0, hot=400.0, cold=300.0):
    return pressure * cold / hot


def check(pressure=10.0, hot=400.0, cold=300.0, volume=0.4):
    # Moles from A, then the pressure those moles exert at the same volume and T_min.
    R = 8.314
    n = pressure * 1.013e5 * volume * 1e-3 / (R * hot)
    return n * R * cold / (volume * 1e-3) / 1.013e5


PARAMS = {"pressure": 10.0, "hot": 400.0, "cold": 300.0}
VARIANTS = [{"cold": 250.0}, {"pressure": 8.0, "hot": 500.0}, {"cold": 360.0}]
ANSWER = 7.5
TOL = 1e-9
