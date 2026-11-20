"""Source p15, MC60: A's boiling elevation exceeds C's by 0.199 C (ค)."""


def solve(benzene_freeze=5.500, solution_freeze=5.010,
          benzene_kf=4.90, benzene_kb=2.50,
          sucrose_mol=0.100, water_kg=1.00, water_kb=0.512):
    benzene_molality = (benzene_freeze - solution_freeze) / benzene_kf
    water_molality = sucrose_mol / water_kg
    return round(benzene_kb * benzene_molality - water_kb * water_molality, 3)


def check(benzene_freeze=5.500, solution_freeze=5.010,
          benzene_kf=4.90, benzene_kb=2.50,
          sucrose_mol=0.100, water_kg=1.00, water_kb=0.512):
    # Reconstruct solute moles from a 50 g benzene sample, then calculate
    # each boiling elevation directly from moles per solvent kilogram.
    solute_mol = (benzene_freeze - solution_freeze) * 0.050 / benzene_kf
    elevation_a = solute_mol * benzene_kb / 0.050
    elevation_c = sucrose_mol * water_kb / water_kg
    assert elevation_a > elevation_c >= 0
    return round(elevation_a - elevation_c, 3)


PARAMS = {"benzene_freeze": 5.500, "solution_freeze": 5.010,
          "benzene_kf": 4.90, "benzene_kb": 2.50,
          "sucrose_mol": 0.100, "water_kg": 1.00, "water_kb": 0.512}
VARIANTS = [
    {**PARAMS, "solution_freeze": 5.108},
    {**PARAMS, "solution_freeze": 4.912},
    {**PARAMS, "sucrose_mol": 0.200},
]
ANSWER = 0.199
