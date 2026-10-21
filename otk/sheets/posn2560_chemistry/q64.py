"""Source p17, written 4: G<E<D<A in metallicity; basic oxides A2E and DE."""


PERIOD_PAIRS = {
    3: ("Na", "Mg"),
    4: ("K", "Ca"),
    5: ("Rb", "Sr"),
    6: ("Cs", "Ba"),
}


def solve(metal_period=3):
    alkali, alkaline = PERIOD_PAIRS[metal_period]
    increasing_metallicity = ("F", "O", alkaline, alkali)
    basic_oxides = (f"{alkali}2O", f"{alkaline}O")
    return increasing_metallicity, basic_oxides


def check(metal_period=3):
    # Independent electronegativity ordering and charge balance for oxides.
    alkali, alkaline = PERIOD_PAIRS[metal_period]
    electronegativity = {
        "F": 3.98, "O": 3.44, "Na": 0.93, "Mg": 1.31,
        "K": 0.82, "Ca": 1.00, "Rb": 0.82, "Sr": 0.95,
        "Cs": 0.79, "Ba": 0.89,
    }
    order = tuple(sorted((alkali, alkaline, "O", "F"),
                         key=lambda symbol: -electronegativity[symbol]))
    # O is 2-; group IA needs two ions, group IIA one ion.
    oxide_formulas = (f"{alkali}2O", f"{alkaline}O")
    return order, oxide_formulas


PARAMS = {"metal_period": 3}
VARIANTS = [
    {"metal_period": 4},
    {"metal_period": 5},
    {"metal_period": 6},
]
ANSWER = (("F", "O", "Mg", "Na"), ("Na2O", "MgO"))
