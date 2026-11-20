"""Lab part 4: Lambda = k d D^2 B^2 for a disc of diameter D over a plate of thickness d, so k = Lambda/(d D^2 B^2); 1.5e-8 over 1 mm, 19 mm and 0.294 T gives 0.48. Adapted: Lambda (units of 1e-8), B and D (mm) vary; returns k."""


def solve(shape=1.5, field=0.294, diameter=19.0, plate=1.0):
    return shape * 1e-8 / (plate * 1e-3 * (diameter * 1e-3) ** 2 * field**2)


def check(shape=1.5, field=0.294, diameter=19.0, plate=1.0):
    # The appendix model: a full disc gives Lambda = (pi/4) d D^2 B^2 from
    # summing strips 2y dx; the measured Lambda over that model, times pi/4.
    from math import pi, sqrt

    R = diameter * 1e-3 / 2
    n = 20000
    area = sum(2 * sqrt(R * R - (-R + (i + 0.5) * 2 * R / n) ** 2) * 2 * R / n for i in range(n))
    model = area * plate * 1e-3 * field**2          # (pi/4) d D^2 B^2
    return shape * 1e-8 / model * pi / 4


PARAMS = {"shape": 1.5, "field": 0.294, "diameter": 19.0, "plate": 1.0}
VARIANTS = [{"field": 0.35}, {"shape": 2.0}, {"diameter": 25.0, "field": 0.25}]
ANSWER = 0.4807169065828605
TOL = 1e-6
