"""Source p6, MC11 has no scientifically correct printed option.

A=O, D=P, E=Ga, G=As. Empirical radii (pm) give Ga>As>P>O;
first ionization energies (eV) give O>P>As>Ga. The printed choices mix
these orders, but none contains both correct comparisons. The adaptation
asks for the corrected full rankings. PubChem element records supply the
empirical/covalent radii; NIST ASD supplies ionization energies.
"""

EMPIRICAL_RADIUS_PM = {"O": 60, "P": 100, "Ga": 130, "As": 115}
FIRST_IE_EV = {"O": 13.618055, "P": 10.486686,
               "Ga": 5.9993020, "As": 9.78855}


def solve(elements=("O", "P", "Ga", "As")):
    if len(elements) != 4 or set(elements) != set(EMPIRICAL_RADIUS_PM):
        raise ValueError("expected a permutation of O, P, Ga, As")
    labels = dict(zip(elements, "ADEG"))
    radius = tuple(labels[symbol] for symbol in sorted(elements,
                    key=EMPIRICAL_RADIUS_PM.get, reverse=True))
    ionization = tuple(labels[symbol] for symbol in sorted(elements,
                        key=FIRST_IE_EV.get, reverse=True))
    return radius, ionization


def check(elements=("O", "P", "Ga", "As")):
    # Different radius definition and independently rounded IE data;
    # derive rankings from pairwise comparisons instead of sorting.
    covalent_radius = {"O": 66, "P": 107, "Ga": 122, "As": 119}
    rounded_ie = {"O": 13.618, "P": 10.487, "Ga": 5.999, "As": 9.815}
    labels = "ADEG"

    def rank(values):
        return tuple(labels[i] for i in sorted(range(4),
                     key=lambda i: sum(values[elements[i]] > values[other]
                                       for other in elements), reverse=True))

    return rank(covalent_radius), rank(rounded_ie)


PARAMS = {"elements": ("O", "P", "Ga", "As")}
VARIANTS = [
    {"elements": ("Ga", "P", "O", "As")},
    {"elements": ("As", "O", "P", "Ga")},
    {"elements": ("P", "As", "Ga", "O")},
]
ANSWER = (("E", "G", "D", "A"), ("A", "D", "G", "E"))
