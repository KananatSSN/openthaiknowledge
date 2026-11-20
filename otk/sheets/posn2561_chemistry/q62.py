"""Source p14, written 2: symbolic atomic-size ranking and ionic formula."""


def solve(d_electrons=6):
    assert d_electrons in (5, 6, 7, 8)
    # n=3: A=Na, D=Mn/Fe/Co/Ni, E=Ca, G=Cl. RSC covalent radii in pm.
    atomic_radii_pm = {"A": 160, "D": {5: 129, 6: 124, 7: 118, 8: 117}[d_electrons],
                       "E": 174, "G": 100}
    smallest = min(atomic_radii_pm, key=atomic_radii_pm.get)
    return smallest, "EG2"


def check(d_electrons=6):
    assert d_electrons in (5, 6, 7, 8)
    # Period-3 chlorine is smaller than Na and the specified period-4 metals.
    period = {"A": 3, "D": 4, "E": 4, "G": 3}
    smallest = "G" if (period["G"] < period["D"] and period["G"] < period["E"]
                       and 17 > 11) else None
    # E has two outer s electrons; G has seven valence electrons.
    e_charge, g_charge = 2, -1
    return smallest, "EG" + str(e_charge // -g_charge)


PARAMS = {"d_electrons": 6}
VARIANTS = [{"d_electrons": 5}, {"d_electrons": 7}, {"d_electrons": 8}]
ANSWER = ("G", "EG2")
