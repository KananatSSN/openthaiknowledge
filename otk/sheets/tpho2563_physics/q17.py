"""Lab part 2.2: interleaving N sheets of each notebook under a load W0 gives T = 2 mu W0 N + T0, so the slope of T against N is 2 mu W0. Two large nuts (W0 = 0.753 N) and the solution's straight part, N = 1 to 8, give a least-squares slope of 0.935 N/sheet and mu = 0.62 (its hand-drawn line has 0.863 N/sheet, mu = 0.57). Adapted: the number of 38.4 g nuts and the readings vary."""

SHEETS = (1, 2, 3, 4, 6, 8)
PULLS = (0.55, 1.50, 2.32, 3.70, 4.74, 7.32)


def solve(nuts=2, sheets=SHEETS, pulls=PULLS):
    from otk.sheets.tpho2563_physics._shared import line

    slope, _ = line(sheets, pulls)
    return slope / (2 * nuts * 38.4e-3 * 9.81)


def check(nuts=2, sheets=SHEETS, pulls=PULLS):
    from otk.sheets.tpho2563_physics._shared import centred_line

    slope, _ = centred_line(sheets, pulls)
    return slope / (2 * nuts * 38.4e-3 * 9.81)


PARAMS = {"nuts": 2, "sheets": SHEETS, "pulls": PULLS}
VARIANTS = [{"nuts": 3}, {"pulls": (0.8, 1.6, 2.5, 3.3, 5.0, 6.6)}, {"sheets": (1, 2, 3, 4, 6, 12)}]
ANSWER = 0.6205137189942237
TOL = 1e-9
