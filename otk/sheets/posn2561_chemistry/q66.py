"""Source p15, written 6: first ionization energy from a Born–Haber cycle."""

from fractions import Fraction


def solve(sublimation=150, dissociation=160, electron_affinity=-300,
          lattice_formation=-1100, formation=-600):
    ionization = (Fraction(formation) - sublimation - Fraction(dissociation, 2)
                  - electron_affinity - lattice_formation)
    assert ionization > 0
    return int(ionization) if ionization.denominator == 1 else ionization


def check(sublimation=150, dissociation=160, electron_affinity=-300,
          lattice_formation=-1100, formation=-600):
    # Independently search the positive integer IE that closes Hess's cycle.
    for candidate in range(1, 3001):
        total = (sublimation + Fraction(dissociation, 2) + candidate
                 + electron_affinity + lattice_formation)
        if total == formation:
            return candidate
    raise AssertionError("no positive integer IE closes the Born–Haber cycle")


PARAMS = {"sublimation": 150, "dissociation": 160,
          "electron_affinity": -300, "lattice_formation": -1100,
          "formation": -600}
VARIANTS = [
    {"sublimation": 120, "dissociation": 200,
     "electron_affinity": -320, "lattice_formation": -900, "formation": -450},
    {"sublimation": 180, "dissociation": 240,
     "electron_affinity": -250, "lattice_formation": -1000, "formation": -500},
    {"sublimation": 100, "dissociation": 180,
     "electron_affinity": -280, "lattice_formation": -800, "formation": -400},
]
ANSWER = 570
