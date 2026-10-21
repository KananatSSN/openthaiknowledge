"""The source does not name a solute; adaptation explicitly takes benzene."""


def solve(benzene_ml=156, toluene_ml=344, benzene_density=0.8, benzene_molar=78):
    return round(
        (benzene_ml * benzene_density / benzene_molar) / ((benzene_ml + toluene_ml) / 1000), 2
    )


def check(benzene_ml=156, toluene_ml=344, benzene_density=0.8, benzene_molar=78):
    mass_benzene = benzene_ml * benzene_density
    mol_benzene = mass_benzene / benzene_molar
    return round(1000 * mol_benzene / (benzene_ml + toluene_ml), 2)


PARAMS = {"benzene_ml": 156, "toluene_ml": 344, "benzene_density": 0.8, "benzene_molar": 78}
VARIANTS = [
    {"benzene_ml": 100, "toluene_ml": 400, "benzene_density": 0.8, "benzene_molar": 78},
    {"benzene_ml": 200, "toluene_ml": 300, "benzene_density": 0.8, "benzene_molar": 78},
    {"benzene_ml": 250, "toluene_ml": 250, "benzene_density": 0.8, "benzene_molar": 78},
]

ANSWER = solve(**PARAMS)
