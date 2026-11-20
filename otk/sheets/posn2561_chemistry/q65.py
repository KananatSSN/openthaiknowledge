"""Source p14, written 5: synthesize Es-248 and calculate remaining mass."""

from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction


def solve(u_mass=238, n_mass=14, initial_mg="10.0", minutes=150):
    neutrons = u_mass + n_mass - 248
    assert 92 + 7 == 99 and neutrons >= 0 and minutes % 25 == 0
    remaining = Fraction(initial_mg) / (2 ** (minutes // 25))
    mass = (Decimal(remaining.numerator) / Decimal(remaining.denominator)).quantize(
        Decimal("0.001"), rounding=ROUND_HALF_UP,
    )
    return neutrons, mass


def check(u_mass=238, n_mass=14, initial_mg="10.0", minutes=150):
    neutron_count = next(count for count in range(10)
                         if 248 + count == u_mass + n_mass)
    mass = Fraction(initial_mg)
    for _ in range(minutes // 25):
        mass /= 2
    rounded = (Decimal(mass.numerator) / Decimal(mass.denominator)).quantize(
        Decimal("0.001"), rounding=ROUND_HALF_UP,
    )
    return neutron_count, rounded


PARAMS = {"u_mass": 238, "n_mass": 14, "initial_mg": "10.0", "minutes": 150}
VARIANTS = [
    {"u_mass": 235, "n_mass": 15, "initial_mg": "8.0", "minutes": 100},
    {"u_mass": 239, "n_mass": 14, "initial_mg": "12.0", "minutes": 75},
    {"u_mass": 238, "n_mass": 15, "initial_mg": "16.0", "minutes": 125},
]
ANSWER = (4, Decimal("0.156"))
