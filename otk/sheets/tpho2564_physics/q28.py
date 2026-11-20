"""Lab part 3 d): T^2 = 16 pi^2 L^3 (a mu L + m)/(E b h^3), so the slope of T^2 against the end mass gives E = 16 pi^2 L^3/(slope b h^3). The solution's 60 cm periods give a least-squares slope of 3.36 s^2/kg and E = 75.7 GPa (the solution: 75.8 GPa). Adapted: the readings vary; returns GPa."""

from math import pi

MASSES = (29.19, 39.59, 49.99, 60.39, 70.79, 81.19, 91.59, 101.99, 112.39, 122.79)
SQUARES = (0.175, 0.214, 0.257, 0.286, 0.323, 0.358, 0.391, 0.430, 0.460, 0.490)


def solve(masses=MASSES, squares=SQUARES, length=60.0):
    from otk.sheets.tpho2564_physics._shared import line
    from otk.sheets.tpho2564_physics.q25 import STRIP

    slope = line([m * 1e-3 for m in masses], squares)[0]
    return 16 * pi**2 * (length * 1e-2) ** 3 / (slope * STRIP["b"] * STRIP["h"] ** 3) / 1e9


def check(masses=MASSES, squares=SQUARES, length=60.0):
    from otk.sheets.tpho2564_physics._shared import centred_line
    from otk.sheets.tpho2564_physics.q25 import STRIP

    slope = centred_line(masses, squares)[0] * 1e3
    return 16 * pi**2 * (length * 1e-2) ** 3 / (slope * STRIP["b"] * STRIP["h"] ** 3) / 1e9


PARAMS = {"masses": MASSES, "squares": SQUARES, "length": 60.0}
VARIANTS = [
    {"squares": (0.180, 0.218, 0.258, 0.292, 0.330, 0.366, 0.401, 0.437, 0.470, 0.505)},
    {"length": 50.0, "squares": (0.100, 0.122, 0.144, 0.166, 0.188, 0.209, 0.231, 0.253, 0.275, 0.297)},
    {"masses": MASSES[:6], "squares": SQUARES[:6]},
]
ANSWER = 75.6850819584148
TOL = 1e-9
