"""Theory 3.1 a), c): the lung obeys p_D = (1/k) ln(alpha/(alpha - V)), so at full inhalation V_f = 3.31 L with alpha_I = 3.58 L and k_I = 0.964e-3 /Pa the pressure difference is 2.67e3 Pa (the solution rounds to 2700 Pa). Adapted: V_f, alpha (L) and k (1e-3 /Pa) vary; returns pascals."""

from math import log


def solve(volume=3.31, alpha=3.58, k=0.964):
    return log(alpha / (alpha - volume)) / (k * 1e-3)


def check(volume=3.31, alpha=3.58, k=0.964):
    from math import exp

    from otk.sheets.tpho2564_physics._shared import bisect

    return bisect(lambda p: alpha * (1 - exp(-k * 1e-3 * p)) - volume, 0.0, 1e5)


PARAMS = {"volume": 3.31, "alpha": 3.58, "k": 0.964}
VARIANTS = [{"volume": 3.0}, {"alpha": 3.57}, {"k": 1.2}]
ANSWER = 2681.2200419049495
TOL = 1e-9
