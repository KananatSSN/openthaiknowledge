"""Lab part 1.2: the intercept of the straight line ln I = ln I0 + eV/(nkT) at V = 0 gives the reverse saturation current I0. Synthetic readings of a green LED (n = 3.0, I0 = 4e-17 A) stand in for the students' data. Adapted: the four (V, I) readings vary; returns amperes."""

from math import exp, log

from otk.sheets.tpho2562_physics.q19 import AMPS, VOLTS


def solve(volts=VOLTS, amps=AMPS):
    from otk.sheets.tpho2562_physics._shared import line

    _, intercept = line(volts, [log(i) for i in amps])
    return exp(intercept)


def check(volts=VOLTS, amps=AMPS):
    from otk.sheets.tpho2562_physics._shared import centred_line

    _, intercept = centred_line(volts, [log(i) for i in amps])
    return exp(intercept)


PARAMS = {"volts": VOLTS, "amps": AMPS}
VARIANTS = [
    {"amps": (1.2e-05, 4.4e-05, 0.00016, 0.00058)},
    {"volts": (2.0, 2.1, 2.2, 2.3)},
    {"amps": (2.0e-05, 0.0001, 0.0005, 0.0025)},
]
ANSWER = 4.0117487877501924e-17
TOL = 1e-6
