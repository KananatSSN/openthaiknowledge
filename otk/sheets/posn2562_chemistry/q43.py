"""MX2 loses X2 gas; conservation of mass yields halogen atomic mass."""


def solve(initial=1.12, residue=0.72, gas_cm3=56.0):
    gas_mol = gas_cm3 / 22400
    return round((initial - residue) / gas_mol / 2)


def check(initial=1.12, residue=0.72, gas_cm3=56.0):
    for atomic_mass in range(1, 201):
        gas_g = (gas_cm3 / 22400) * 2 * atomic_mass
        if abs(residue + gas_g - initial) < 1e-8:
            return atomic_mass
    raise ValueError("no atomic mass fits")


PARAMS = {"initial": 1.12, "residue": 0.72, "gas_cm3": 56.0}
VARIANTS = [
    {"initial": 2.24, "residue": 1.44, "gas_cm3": 112.0},
    {"initial": 1.02, "residue": 0.72, "gas_cm3": 56.0},
    {"initial": 1.32, "residue": 0.72, "gas_cm3": 56.0},
]
ANSWER = solve(**PARAMS)
