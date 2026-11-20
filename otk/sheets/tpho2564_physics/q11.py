"""Theory 2 d): between the plates V = k x^(4/3), so at a depth x the potential is V_d (x/d)^(4/3). Adapted: V_d and the fraction x/d vary; returns volts."""


def solve(volts=100.0, fraction=0.5):
    return volts * fraction ** (4 / 3)


def check(volts=100.0, fraction=0.5, side=5.0, gap=10.0):
    from otk.sheets.tpho2564_physics import q10
    from otk.sheets.tpho2564_physics._shared import bisect, gap_for

    # with the Child-Langmuir current, find the potential reached at x
    current = q10.solve(volts=volts, side=side, gap=gap) * 1e-3
    target = fraction * gap * 1e-3
    return bisect(lambda v: gap_for(current, v, side * 1e-2) - target, 1e-9, volts)


PARAMS = {"volts": 100.0, "fraction": 0.5}
VARIANTS = [{"fraction": 0.25}, {"volts": 300.0}, {"fraction": 0.8}]
ANSWER = 39.68502629920499
TOL = 1e-6
