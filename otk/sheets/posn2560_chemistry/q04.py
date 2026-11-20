"""Source p4, MC4: B2+ has 10 electrons and 15 neutrons; A has 5 fewer neutrons.

Return (atomic number, mass number) of isotope A. The source symbol is
therefore 22/12 A. Charge is signed: a negative value means an anion.
"""


def solve(electrons=10, charge=2, neutrons=15, fewer=5):
    atomic = electrons + charge
    a_neutrons = neutrons - fewer
    if atomic < 1 or a_neutrons < 0 or fewer < 0:
        raise ValueError("invalid isotope data")
    return atomic, atomic + a_neutrons


def check(electrons=10, charge=2, neutrons=15, fewer=5):
    # Search whole nuclei and test charge and isotope constraints directly.
    for protons in range(1, electrons + abs(charge) + 2):
        for mass in range(protons, protons + neutrons + 1):
            if protons - electrons == charge and neutrons - (mass - protons) == fewer:
                return protons, mass
    raise ValueError("no nucleus satisfies the data")


PARAMS = {"electrons": 10, "charge": 2, "neutrons": 15, "fewer": 5}
VARIANTS = [
    {"electrons": 18, "charge": 3, "neutrons": 24, "fewer": 2},
    {"electrons": 10, "charge": -1, "neutrons": 12, "fewer": 0},
    {"electrons": 18, "charge": -2, "neutrons": 20, "fewer": 4},
]
ANSWER = (12, 22)
