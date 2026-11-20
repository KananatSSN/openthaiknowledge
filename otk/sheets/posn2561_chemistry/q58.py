"""Source p13, MC58: identify a gas from density and the fastest diffuser."""

from fractions import Fraction


MOLAR_MASS = {"PF3": 88, "PF5": 126, "P2F4": 138}
R = Fraction("0.082")


def solve(density="4.60", pressure="0.82", temperature_c=27):
    implied = Fraction(density) * R * (temperature_c + 273) / Fraction(pressure)
    dense = min(MOLAR_MASS, key=lambda gas: abs(MOLAR_MASS[gas] - implied))
    fastest = min(MOLAR_MASS, key=MOLAR_MASS.get)
    assert abs(MOLAR_MASS[dense] - implied) < 1
    return dense, fastest


def check(density="4.60", pressure="0.82", temperature_c=27):
    observed = Fraction(density)
    candidates = {
        gas: abs(Fraction(mass) * Fraction(pressure)
                 / (R * (temperature_c + 273)) - observed)
        for gas, mass in MOLAR_MASS.items()
    }
    dense = min(candidates, key=candidates.get)
    # At equal temperature, a lighter molecule crosses the same distance faster.
    fast = max(MOLAR_MASS, key=lambda gas: Fraction(1, MOLAR_MASS[gas]))
    return dense, fast


PARAMS = {"density": "4.60", "pressure": "0.82", "temperature_c": 27}
VARIANTS = [
    {"density": "4.20", "pressure": "0.82", "temperature_c": 27},
    {"density": "4.40", "pressure": "1.23", "temperature_c": 27},
    {"density": "6.90", "pressure": "1.23", "temperature_c": 27},
]
ANSWER = ("P2F4", "PF3")
