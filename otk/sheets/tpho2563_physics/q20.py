"""Lab part 3.2: the constant k = 2 mu delta N^2 with paper 0.106 mm thick and N = 24 sheets, so k = 0.042 m gives mu = k/(2 delta N^2) = 0.34. Adapted: k (m), the sheet count and the thickness (mm) vary."""


def solve(k=0.042, sheets=24, thickness=0.106):
    return k / (2 * thickness * 1e-3 * sheets**2)


def check(k=0.042, sheets=24, thickness=0.106):
    from otk.sheets.tpho2563_physics._shared import bisect

    return bisect(lambda mu: 2 * mu * thickness * 1e-3 * sheets**2 - k, 0.0, 10.0)


PARAMS = {"k": 0.042, "sheets": 24, "thickness": 0.106}
VARIANTS = [{"k": 0.06}, {"sheets": 20}, {"thickness": 0.09}]
ANSWER = 0.3439465408805032
TOL = 1e-9
