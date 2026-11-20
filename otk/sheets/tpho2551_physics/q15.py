"""Lab 2 figure: a potentiometer balanced with the standard cell E_s across resistance R_s and with the unknown E_x across R_x (same working current) gives E_x = (R_x/R_s) E_s. Adapted: synthetic balance resistances with E_s = 1.65 V; volts."""


def solve(unknown=520, standard=600, cell=1.65):
    return unknown / standard * cell


def check(unknown=520, standard=600, cell=1.65):
    # Bisect on the working current until the galvanometer reads zero with the
    # standard cell across R_s; the same current across R_x then balances E_x.
    lo, hi = 0.0, 1.0
    for _ in range(200):
        current = (lo + hi) / 2
        lo, hi = (current, hi) if current * standard < cell else (lo, current)
    return lo * unknown


PARAMS = {"unknown": 520, "standard": 600, "cell": 1.65}
VARIANTS = [{"unknown": 900}, {"standard": 330, "unknown": 300}, {"unknown": 1000, "standard": 1100}]
ANSWER = 1.43
TOL = 1e-12
