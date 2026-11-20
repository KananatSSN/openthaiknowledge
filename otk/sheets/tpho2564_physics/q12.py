"""Theory 2 f): rho = -eps0 V'' integrated across the gap gives the space charge Q = -eps0 a^2 (E at the anode) = -(4/3) eps0 a^2 V_d/d. Adapted: V_d, the plate side a (cm) and gap d (mm) vary; returns nanocoulombs."""


def solve(volts=100.0, side=5.0, gap=10.0):
    from otk.sheets.tpho2564_physics._shared import EPS0

    return -4 / 3 * EPS0 * (side * 1e-2) ** 2 * volts / (gap * 1e-3) * 1e9


def check(volts=100.0, side=5.0, gap=10.0):
    from otk.sheets.tpho2564_physics import q10
    from otk.sheets.tpho2564_physics._shared import EPS0, alpha_for

    # V' at the anode from the first integral (V')^2 = 4 alpha sqrt(V); V'(0) = 0
    alpha = alpha_for(q10.check(volts=volts, side=side, gap=gap) * 1e-3, side * 1e-2)
    slope = 2 * alpha**0.5 * volts**0.25
    return -EPS0 * (side * 1e-2) ** 2 * slope * 1e9


PARAMS = {"volts": 100.0, "side": 5.0, "gap": 10.0}
VARIANTS = [{"volts": 400.0}, {"side": 2.0}, {"gap": 3.0}]
ANSWER = -0.2951333333333334
TOL = 1e-6
