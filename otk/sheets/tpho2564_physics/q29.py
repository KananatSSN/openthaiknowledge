"""Lab part 3 d): the line T^2 = slope (m + a mu L) cuts the mass axis at -a mu L, so a = -x0/(mu L) with mu L = 0.122 x 0.60 = 73.2 g; the solution's least-squares x0 = -24.61 g gives a = 0.336 (theory 0.24). Adapted: the readings vary."""

from otk.sheets.tpho2564_physics.q28 import MASSES, SQUARES


def solve(masses=MASSES, squares=SQUARES, length=60.0):
    from otk.sheets.tpho2564_physics._shared import line

    slope, intercept = line(masses, squares)
    return intercept / slope / (122.0 * length * 1e-2)


def check(masses=MASSES, squares=SQUARES, length=60.0):
    from otk.sheets.tpho2564_physics import q28
    from otk.sheets.tpho2564_physics._shared import centred_line
    from otk.sheets.tpho2564_physics.q25 import STRIP

    # the solution's second route: the T^2 intercept with E from the slope
    from math import pi

    _, intercept = centred_line(masses, squares)
    modulus = q28.check(masses=masses, squares=squares, length=length) * 1e9
    L = length * 1e-2
    beam = intercept * modulus * STRIP["b"] * STRIP["h"] ** 3 / (16 * pi**2 * L**3)  # kg
    return beam / (STRIP["mu"] * L)


PARAMS = {"masses": MASSES, "squares": SQUARES, "length": 60.0}
VARIANTS = [
    {"squares": (0.180, 0.218, 0.258, 0.292, 0.330, 0.366, 0.401, 0.437, 0.470, 0.505)},
    {"length": 50.0, "squares": (0.100, 0.122, 0.144, 0.166, 0.188, 0.209, 0.231, 0.253, 0.275, 0.297)},
    {"masses": MASSES[:6], "squares": SQUARES[:6]},
]
ANSWER = 0.3362760301284903
TOL = 1e-9
