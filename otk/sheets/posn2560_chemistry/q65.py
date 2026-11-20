"""Source p17, written 5: lattice-formation enthalpy of MG2 is -2535 kJ/mol."""


def solve(sublimation=150, first_ie=750, second_ie=1450,
          dissociation=245, electron_affinity=-350, formation=-640):
    gaseous_ion_cost = (sublimation + first_ie + second_ie
                        + dissociation + 2 * electron_affinity)
    return formation - gaseous_ion_cost


def check(sublimation=150, first_ie=750, second_ie=1450,
          dissociation=245, electron_affinity=-350, formation=-640):
    # Step through the Born-Haber cycle for one formula unit, including
    # electron capture by *both* G atoms, then balance the formation path.
    energy = 0
    for change in (sublimation, first_ie, second_ie, dissociation,
                   electron_affinity, electron_affinity):
        energy += change
    lattice_formation = formation - energy
    assert energy + lattice_formation == formation
    return lattice_formation


PARAMS = {"sublimation": 150, "first_ie": 750, "second_ie": 1450,
          "dissociation": 245, "electron_affinity": -350, "formation": -640}
VARIANTS = [
    {"sublimation": 160, "first_ie": 700, "second_ie": 1400,
     "dissociation": 200, "electron_affinity": -300, "formation": -600},
    {"sublimation": 120, "first_ie": 800, "second_ie": 1500,
     "dissociation": 240, "electron_affinity": -400, "formation": -700},
    {"sublimation": 180, "first_ie": 650, "second_ie": 1300,
     "dissociation": 300, "electron_affinity": -325, "formation": -500},
]
ANSWER = -2535
