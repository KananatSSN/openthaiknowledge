"""Theory 2 g): the field vanishes at the cathode (sigma- = 0) and is (4/3) V_d/d at the anode, so sigma+ = +(4/3) eps0 V_d/d, which balances the space charge. (The solution's first method writes a minus sign; its second method and charge neutrality give plus.) Adapted: V_d and the gap d (mm) vary; returns nC/m^2."""


def solve(volts=100.0, gap=10.0):
    from otk.sheets.tpho2564_physics._shared import EPS0

    return 4 / 3 * EPS0 * volts / (gap * 1e-3) * 1e9


def check(volts=100.0, gap=10.0, side=5.0):
    from otk.sheets.tpho2564_physics import q12

    # neutrality: a^2 sigma+ + Q + a^2 sigma- = 0 with sigma- = 0
    return -q12.check(volts=volts, side=side, gap=gap) / (side * 1e-2) ** 2


PARAMS = {"volts": 100.0, "gap": 10.0}
VARIANTS = [{"volts": 400.0}, {"gap": 3.0}, {"volts": 50.0, "gap": 20.0}]
ANSWER = 118.05333333333331
TOL = 1e-6
