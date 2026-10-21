"""Source p3, MC2: X3+ has 10 electrons and neutral X has 14 neutrons."""


def solve(neutrons=14, ion_electrons=10, charge=3):
    atomic = ion_electrons + charge
    return atomic, atomic + neutrons


def check(neutrons=14, ion_electrons=10, charge=3):
    # Search the element and isotope that satisfy both observations.
    candidates = [(protons, mass) for protons in range(1, 60)
                  for mass in range(protons, protons + 80)
                  if mass - protons == neutrons
                  and protons - charge == ion_electrons]
    assert len(candidates) == 1
    return candidates[0]


PARAMS = {"neutrons": 14, "ion_electrons": 10, "charge": 3}
VARIANTS = [
    {"neutrons": 12, "ion_electrons": 10, "charge": 2},
    {"neutrons": 16, "ion_electrons": 18, "charge": 1},
    {"neutrons": 20, "ion_electrons": 18, "charge": 2},
]
ANSWER = (13, 27)
