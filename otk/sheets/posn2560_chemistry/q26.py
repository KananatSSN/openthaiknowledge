"""Source p9, MC26: CaCO3 has ionic and covalent bonding (choice ง)."""

_BONDS = {
    "Na2O": (True, False), "COCl2": (False, True),
    "H2SO4": (False, True), "CaCO3": (True, True),
    "NaNO3": (True, True), "NH4Cl": (True, True),
    "K2SO4": (True, True), "NaCl": (True, False),
    "H2O": (False, True), "CO2": (False, True),
}

# Separate structural audit: polyatomic ions have covalent bonds within
# the ion and electrostatic bonding to their counterion in the solid salt.
_IONS = {
    "Na2O": ("Na+", "O2-"), "CaCO3": ("Ca2+", "CO3^2-"),
    "NaNO3": ("Na+", "NO3-"), "NH4Cl": ("NH4+", "Cl-"),
    "K2SO4": ("K+", "SO4^2-"), "NaCl": ("Na+", "Cl-"),
}
_POLYATOMIC = {"CO3^2-", "NO3-", "NH4+", "SO4^2-"}


def solve(compounds=("Na2O", "COCl2", "H2SO4", "CaCO3")):
    matches = [item for item in compounds if _BONDS[item] == (True, True)]
    assert len(matches) == 1
    return matches[0]


def check(compounds=("Na2O", "COCl2", "H2SO4", "CaCO3")):
    matches = [item for item in compounds if item in _IONS
               and any(ion in _POLYATOMIC for ion in _IONS[item])]
    assert len(matches) == 1
    return matches[0]


PARAMS = {"compounds": ("Na2O", "COCl2", "H2SO4", "CaCO3")}
VARIANTS = [
    {"compounds": ("NaNO3", "NaCl", "H2O", "COCl2")},
    {"compounds": ("H2SO4", "NH4Cl", "Na2O", "CO2")},
    {"compounds": ("NaCl", "CO2", "K2SO4", "H2O")},
]
ANSWER = "CaCO3"
