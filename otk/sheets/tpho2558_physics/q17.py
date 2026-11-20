"""Lab part 3: a drop leaves the needle when mg = 1.4 (pi r_o) gamma with the needle's outer radius r_o = r + wall; 50 drops of 1.20 ml with r_o = 0.645 mm give gamma = rho V g/(1.4 pi r_o) = 83.6 mN/m. Adapted: the number of drops, their volume (ml) and the bore radius (mm) vary with a 0.220 mm wall; returns gamma in mN/m (rho = 1030 kg/m^3)."""

from math import pi


def solve(drops=50, volume=1.20, radius=0.425, wall=0.220, rho=1030.0, g=9.8):
    each = volume * 1e-6 / drops
    return rho * each * g / (1.4 * pi * (radius + wall) * 1e-3) * 1e3


def check(drops=50, volume=1.20, radius=0.425, wall=0.220, rho=1030.0, g=9.8):
    # Bisect gamma until the pinch-off force equals one drop's weight.
    from otk.sheets.tpho2558_physics._shared import bisect

    weight = rho * volume * 1e-6 / drops * g
    ro = (radius + wall) * 1e-3
    return bisect(lambda t: 1.4 * pi * ro * t - weight, 0.0, 10.0) * 1e3


PARAMS = {"drops": 50, "volume": 1.20, "radius": 0.425, "wall": 0.220, "rho": 1030.0, "g": 9.8}
VARIANTS = [{"drops": 40}, {"volume": 1.5}, {"radius": 0.40, "volume": 1.1}]
ANSWER = 85.39588016316767
TOL = 1e-9
