"""Lab part 1.2: at low current I = I0 exp(eV/(nkT)), so ln I against V is a straight line of slope e/(nkT) and n = e/(kT x slope). Synthetic readings of a green LED (n = 3.0, I0 = 4e-17 A) stand in for the students' data. Adapted: the four (V, I) readings vary; returns the ideality factor at T = 300 K."""

from math import log

VOLTS = (2.20, 2.30, 2.40, 2.50)
AMPS = (8.14e-05, 0.000295, 0.00107, 0.00388)


def solve(volts=VOLTS, amps=AMPS):
    from otk.sheets.tpho2562_physics._shared import E, K_B, line

    slope, _ = line(volts, [log(i) for i in amps])
    return E / (K_B * 300 * slope)


def check(volts=VOLTS, amps=AMPS):
    from otk.sheets.tpho2562_physics._shared import E, K_B, centred_line

    slope, _ = centred_line(volts, [log(i) for i in amps])
    return E / (K_B * 300 * slope)


PARAMS = {"volts": VOLTS, "amps": AMPS}
VARIANTS = [
    {"amps": (1.2e-05, 4.4e-05, 0.00016, 0.00058)},
    {"volts": (2.0, 2.1, 2.2, 2.3)},
    {"amps": (2.0e-05, 0.0001, 0.0005, 0.0025)},
]
ANSWER = 3.0003175854859983
TOL = 1e-9
