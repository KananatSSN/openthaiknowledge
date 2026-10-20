"""Theory 2 i): two neighbouring moments 1 nm away, aligned, give B_L ~ 2 (mu0/4 pi) mu/r^3 = 1.85 mT (the solution rounds to 2 mT). Adapted: the spacing (nm) and the number of neighbours vary; returns mT."""

from math import pi


def solve(spacing=1.0, neighbours=2):
    from otk.sheets.tpho2565_physics._shared import BOHR, MU0

    return neighbours * MU0 / (4 * pi) * BOHR / (spacing * 1e-9) ** 3 * 1e3


def check(spacing=1.0, neighbours=2):
    from otk.sheets.tpho2565_physics._shared import BOHR

    # mu0/(4 pi) is exactly 1e-7 T m/A
    one = 1e-7 * BOHR / (spacing * 1e-9) ** 3
    return sum(one for _ in range(neighbours)) * 1e3


PARAMS = {"spacing": 1.0, "neighbours": 2}
VARIANTS = [{"spacing": 0.5}, {"neighbours": 4}, {"spacing": 2.0}]
ANSWER = 1.8548
TOL = 1e-9
