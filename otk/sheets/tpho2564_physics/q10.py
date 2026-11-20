"""Theory 2 c)-e): in steady state V'' = (I/(eps0 a^2)) sqrt(m/(2 e V)), solved by V = k x^(4/3), so the space-charge-limited current is I = (4 eps0 a^2/(9 d^2)) sqrt(2e/m) V_d^(3/2). Adapted: V_d, the plate side a (cm) and gap d (mm) vary; returns mA."""

from math import sqrt


def solve(volts=100.0, side=5.0, gap=10.0):
    from otk.sheets.tpho2564_physics._shared import CHARGE, ELECTRON, EPS0

    a, d = side * 1e-2, gap * 1e-3
    return 4 * EPS0 * a * a / (9 * d * d) * sqrt(2 * CHARGE / ELECTRON) * volts**1.5 * 1e3


def check(volts=100.0, side=5.0, gap=10.0):
    from math import log, exp

    from otk.sheets.tpho2564_physics._shared import bisect, gap_for

    # the current for which Poisson's equation spans exactly the gap
    def miss(log_i):
        return gap_for(exp(log_i), volts, side * 1e-2) - gap * 1e-3

    return exp(bisect(miss, log(1e-9), log(1e3), n=120)) * 1e3


PARAMS = {"volts": 100.0, "side": 5.0, "gap": 10.0}
VARIANTS = [{"volts": 400.0}, {"side": 2.0}, {"gap": 3.0}]
ANSWER = 58.3455732089198
TOL = 1e-6
