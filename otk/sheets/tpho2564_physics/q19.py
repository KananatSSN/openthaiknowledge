"""Theory 3.1 h): breathing out along alpha_O = 3.35 L, k_O = 1.644e-3 /Pa returns w_O = -(alpha_O/k_O)[1 - exp(-x)(1 + x)], x = ln(alpha_O/(alpha_O - V_f)), so the heat over the net work of one breath is Q/(w_I + w_O): 31.4 here (the solution's w_O = -1.94 J gives 32.6; the ratio is sensitive to alpha_O as V_f = 3.31 L is close to it). Adapted: the volume (L) and both alphas (L) vary."""

from math import exp, log


def solve(volume=3.31, inhale=3.58, exhale=3.35):
    from otk.sheets.tpho2564_physics import q15, q18

    x = log(exhale / (exhale - volume))
    back = -exhale / 1.644 * (1 - exp(-x) * (1 + x))
    return q18.solve(volume=volume, alpha=inhale) / (q15.solve(volume=volume, alpha=inhale) + back)


def check(volume=3.31, inhale=3.58, exhale=3.35):
    from otk.sheets.tpho2564_physics import q15, q18

    # the exhaled work is minus the same integral along the exhale curve
    back = -q15.check(volume=volume, alpha=exhale, k=1.644)
    return q18.check(volume=volume, alpha=inhale) / (q15.check(volume=volume, alpha=inhale) + back)


PARAMS = {"volume": 3.31, "inhale": 3.58, "exhale": 3.35}
VARIANTS = [{"exhale": 3.4}, {"volume": 3.2}, {"inhale": 3.65}]
ANSWER = 30.96491536133882
TOL = 1e-4
