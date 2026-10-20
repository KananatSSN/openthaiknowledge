"""Theory 1.2 (a) figure: at T0 the weight stretches the wire by Delta L1 = W L0/(A Y0). Adapted: W (N), L0 (m), A (mm^2) and Y0 (GPa) vary; returns Delta L1 in mm."""


def solve(weight=100.0, length=2.0, area=1.0, modulus=200.0):
    return weight * length / (area * 1e-6 * modulus * 1e9) * 1e3


def check(weight=100.0, length=2.0, area=1.0, modulus=200.0):
    # Hooke's law as a spring: k = Y A/L, stretch = W/k, bisected.
    from otk.sheets.tpho2559_physics._shared import bisect

    k = modulus * 1e9 * area * 1e-6 / length
    return bisect(lambda x: k * x - weight, 0.0, 1.0) * 1e3


PARAMS = {"weight": 100.0, "length": 2.0, "area": 1.0, "modulus": 200.0}
VARIANTS = [{"weight": 250.0}, {"area": 0.5, "length": 3.0}, {"modulus": 70.0}]
ANSWER = 1.0000000000000002
TOL = 1e-9
