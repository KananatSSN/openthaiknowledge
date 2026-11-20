"""Source p19, written 10: freezing depression gives 118 g/mol and 1.50 m."""


def solve(solute_g=17.7, water_g=100.0, solution_freeze_c=-2.79,
          pure_freeze_c=0.0, kf=1.86):
    depression = pure_freeze_c - solution_freeze_c
    molality = depression / kf
    solute_mol = molality * water_g / 1000
    return round(solute_g / solute_mol, 1), round(molality, 2)


def check(solute_g=17.7, water_g=100.0, solution_freeze_c=-2.79,
          pure_freeze_c=0.0, kf=1.86):
    # Independently invert the predicted freezing depression by bisection
    # over molar mass; then back-calculate molality from the recovered moles.
    observed = pure_freeze_c - solution_freeze_c
    assert observed > 0 and solute_g > 0 and water_g > 0
    low, high = 1.0, 1000.0
    for _ in range(60):
        trial = (low + high) / 2
        predicted = kf * (solute_g / trial) / (water_g / 1000)
        if predicted > observed:
            low = trial
        else:
            high = trial
    molar_mass = (low + high) / 2
    molality = (solute_g / molar_mass) / (water_g / 1000)
    return round(molar_mass, 1), round(molality, 2)


PARAMS = {"solute_g": 17.7, "water_g": 100.0,
          "solution_freeze_c": -2.79, "pure_freeze_c": 0.0, "kf": 1.86}
VARIANTS = [
    {"solute_g": 12.0, "water_g": 100.0,
     "solution_freeze_c": -1.86, "pure_freeze_c": 0.0, "kf": 1.86},
    {"solute_g": 18.0, "water_g": 200.0,
     "solution_freeze_c": -1.86, "pure_freeze_c": 0.0, "kf": 1.86},
    {"solute_g": 30.0, "water_g": 250.0,
     "solution_freeze_c": -3.72, "pure_freeze_c": 0.0, "kf": 1.86},
]
ANSWER = (118.0, 1.50)
