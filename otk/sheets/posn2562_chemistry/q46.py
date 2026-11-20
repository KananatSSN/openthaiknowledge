"""Hydrolysis products determine A:X:Z as 1:1:3."""


def solve(sample_g=40.9, acid_g=14.6, hz_g=27.3, a_mass=79, x_mass=60, z_mass=90):
    a_mol = acid_g / (3 + a_mass + 64)
    z_mol = hz_g / (1 + z_mass)
    x_mol = (sample_g - a_mol * a_mass - z_mol * z_mass) / x_mass
    return tuple(round(m / a_mol) for m in (a_mol, x_mol, z_mol))


def check(sample_g=40.9, acid_g=14.6, hz_g=27.3, a_mass=79, x_mass=60, z_mass=90):
    for z in range(1, 8):
        formula_mass = a_mass + x_mass + z * z_mass
        formula_mol = sample_g / formula_mass
        if (
            abs(formula_mol * (a_mass + 67) - acid_g) < 1e-7
            and abs(formula_mol * z * (z_mass + 1) - hz_g) < 1e-7
        ):
            return (1, 1, z)
    raise ValueError("no empirical formula")


PARAMS = {"sample_g": 40.9, "acid_g": 14.6, "hz_g": 27.3, "a_mass": 79, "x_mass": 60, "z_mass": 90}
VARIANTS = [
    {"sample_g": 81.8, "acid_g": 29.2, "hz_g": 54.6, "a_mass": 79, "x_mass": 60, "z_mass": 90},
    {"sample_g": 20.45, "acid_g": 7.3, "hz_g": 13.65, "a_mass": 79, "x_mass": 60, "z_mass": 90},
    {"sample_g": 122.7, "acid_g": 43.8, "hz_g": 81.9, "a_mass": 79, "x_mass": 60, "z_mass": 90},
]
ANSWER = solve(**PARAMS)
