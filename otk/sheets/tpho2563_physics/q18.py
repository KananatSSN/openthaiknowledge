"""Lab part 2.2: the intercept of T = 2 mu W0 N + T0 gives the other friction T0 of the set-up; the solution's points N = 1 to 8 give -0.385 N by least squares (its hand-drawn line gives -0.1 +- 0.2 N). Adapted: the readings vary; returns newtons."""

from otk.sheets.tpho2563_physics.q17 import PULLS, SHEETS


def solve(sheets=SHEETS, pulls=PULLS):
    from otk.sheets.tpho2563_physics._shared import line

    return line(sheets, pulls)[1]


def check(sheets=SHEETS, pulls=PULLS):
    from otk.sheets.tpho2563_physics._shared import centred_line

    return centred_line(sheets, pulls)[1]


PARAMS = {"sheets": SHEETS, "pulls": PULLS}
VARIANTS = [{"pulls": (0.8, 1.6, 2.5, 3.3, 5.0, 6.6)}, {"sheets": (1, 2, 3, 4, 6, 12)}, {"pulls": (0.4, 1.2, 2.0, 2.9, 4.5, 6.1)}]
ANSWER = -0.38499999999999984
TOL = 1e-6
