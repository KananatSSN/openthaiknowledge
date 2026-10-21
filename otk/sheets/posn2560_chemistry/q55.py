"""Source p13, MC55: 3.50 M sulfuric acid at 1.20 g/mL is 4.08 m (ค)."""


def solve(molar=3.50, density=1.20):
    # Work with a litre of solution: its mass is 1000*density grams.
    acid_g = molar * 98
    solvent_kg = (1000 * density - acid_g) / 1000
    assert solvent_kg > 0
    return round(molar / solvent_kg, 2)


def check(molar=3.50, density=1.20):
    # Independent 100 mL sample: moles divided by solvent kilograms.
    sample_acid_mol = molar / 10
    sample_water_g = 100 * density - sample_acid_mol * (2 + 32 + 4 * 16)
    return round(1000 * sample_acid_mol / sample_water_g, 2)


PARAMS = {"molar": 3.50, "density": 1.20}
VARIANTS = [
    {"molar": 2.00, "density": 1.10},
    {"molar": 4.00, "density": 1.30},
    {"molar": 1.50, "density": 1.05},
]
ANSWER = 4.08
