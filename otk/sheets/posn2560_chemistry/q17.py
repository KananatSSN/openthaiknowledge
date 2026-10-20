"""Source p7, MC17: hydrogen has one valence electron, halogens seven (ค).

The source's other properties are shared by H and several halogens, but
fluorine is an exception to the 'multiple oxidation states' distractor.
The adaptation asks directly for the two valence-electron counts.
"""

_VALENCE = {"H": 1, "F": 7, "Cl": 7, "Br": 7, "I": 7}


def solve(halogen="Cl"):
    return _VALENCE["H"], _VALENCE[halogen]


def check(halogen="Cl"):
    shells = {"H": (1,), "F": (2, 7), "Cl": (2, 8, 7),
              "Br": (2, 8, 18, 7), "I": (2, 8, 18, 18, 7)}
    return shells["H"][-1], shells[halogen][-1]


PARAMS = {"halogen": "Cl"}
VARIANTS = [{"halogen": "F"}, {"halogen": "Br"}, {"halogen": "I"}]
ANSWER = (1, 7)
