"""Equal atoms when mass and molar mass both double."""


def solve(a_mass=40, d_mass=80, d_sample_multiple=2):
    from fractions import Fraction

    return Fraction(d_sample_multiple * a_mass, d_mass)


def check(a_mass=40, d_mass=80, d_sample_multiple=2):
    from fractions import Fraction

    a_mol = Fraction(1, a_mass)
    d_mol = Fraction(d_sample_multiple, d_mass)
    return d_mol / a_mol


PARAMS = {"a_mass": 40, "d_mass": 80, "d_sample_multiple": 2}
VARIANTS = [
    {"a_mass": 20, "d_mass": 40, "d_sample_multiple": 2},
    {"a_mass": 50, "d_mass": 100, "d_sample_multiple": 2},
    {"a_mass": 30, "d_mass": 60, "d_sample_multiple": 2},
]
ANSWER = solve(**PARAMS)
