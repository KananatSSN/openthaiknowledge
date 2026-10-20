"""Theory 1.2 (c)-(d): Delta L2 = Delta L1 to first order in Delta T gives (W/(A Y0))(alpha - epsilon/Y0) + alpha = 0, so A = (W/Y0)(epsilon/(alpha Y0) - 1), possible only when epsilon > 0 (material 1). Adapted: W (N), Y0 (GPa), epsilon (MPa/K) and alpha (1e-6/K) vary; returns A in mm^2."""


def solve(weight=100.0, modulus=200.0, slope=50.0, expansion=12.0):
    Y0, e, a = modulus * 1e9, slope * 1e6, expansion * 1e-6
    return weight / Y0 * (e / (a * Y0) - 1) * 1e6


def check(weight=100.0, modulus=200.0, slope=50.0, expansion=12.0, length=2.0):
    # Bisect the area whose exact stretch at a tiny warming equals the stretch at T0.
    from otk.sheets.tpho2559_physics._shared import bisect

    dT = 1e-4
    Y0, e, a = modulus * 1e9, slope * 1e6, expansion * 1e-6

    def gap(A):
        cold = weight * length / (A * Y0)
        warm = weight * length * (1 + a * dT) / (A * (Y0 + e * dT)) + a * length * dT
        return cold - warm

    return bisect(gap, 1e-12, 1e-2) * 1e6


PARAMS = {"weight": 100.0, "modulus": 200.0, "slope": 50.0, "expansion": 12.0}
VARIANTS = [{"weight": 300.0}, {"slope": 80.0}, {"expansion": 8.0, "modulus": 150.0}]
ANSWER = 0.009916666666666666
TOL = 1e-5
