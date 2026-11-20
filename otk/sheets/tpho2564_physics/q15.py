"""Theory 3.1 c): the work to stretch the lung is w = integral of p_D dV with V = alpha(1 - exp(-k p)), giving (alpha/k)[1 - exp(-k p_f)(1 + k p_f)] = 2.70 J for V_f = 3.31 L, alpha_I = 3.58 L, k_I = 0.964e-3 /Pa. Adapted: V_f, alpha (L) and k (1e-3 /Pa) vary; returns joules."""

from math import exp


def solve(volume=3.31, alpha=3.58, k=0.964):
    from otk.sheets.tpho2564_physics import q14

    x = k * 1e-3 * q14.solve(volume=volume, alpha=alpha, k=k)
    return alpha * 1e-3 / (k * 1e-3) * (1 - exp(-x) * (1 + x))


def check(volume=3.31, alpha=3.58, k=0.964, steps=20000):
    from math import log

    # sum p_D dV over the volume in thin slices
    dv = volume / steps
    return sum(log(alpha / (alpha - (i + 0.5) * dv)) / (k * 1e-3) * dv * 1e-3 for i in range(steps))


PARAMS = {"volume": 3.31, "alpha": 3.58, "k": 0.964}
VARIANTS = [{"volume": 3.0}, {"alpha": 3.57}, {"k": 1.2}]
ANSWER = 2.709680547191888
TOL = 1e-6
