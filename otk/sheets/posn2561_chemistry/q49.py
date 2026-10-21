"""Source p11, MC49: molar mass from benzene boiling-point elevation."""

from fractions import Fraction


def solve(solute_g="2.80", benzene_g="32.0", rise_c="1.40", kb="2.53"):
    assert min(map(Fraction, (solute_g, benzene_g, rise_c, kb))) > 0
    molar_mass = Fraction(solute_g) * Fraction(kb) * 1000
    molar_mass /= Fraction(rise_c) * Fraction(benzene_g)
    return int(molar_mass + Fraction(1, 2))


def check(solute_g="2.80", benzene_g="32.0", rise_c="1.40", kb="2.53"):
    # Forward-predict the boiling rise at each integer g/mol candidate.
    target = Fraction(rise_c)
    def prediction(mass):
        solute_mol = Fraction(solute_g) / mass
        solvent_kg = Fraction(benzene_g) / 1000
        return Fraction(kb) * solute_mol / solvent_kg
    return min(range(1, 501), key=lambda mass: abs(prediction(mass) - target))


PARAMS = {"solute_g": "2.80", "benzene_g": "32.0", "rise_c": "1.40", "kb": "2.53"}
VARIANTS = [
    {"solute_g": "2.40", "benzene_g": "40.0", "rise_c": "2.53", "kb": "2.53"},
    {"solute_g": "2.00", "benzene_g": "40.0", "rise_c": "1.265", "kb": "2.53"},
    {"solute_g": "3.00", "benzene_g": "50.0", "rise_c": "1.265", "kb": "2.53"},
]
ANSWER = 158
