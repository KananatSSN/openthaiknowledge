"""Source p9, MC27: O3 admits the textbook O=O→O drawing (choice ข).

The arrow records electron-pair bookkeeping in one Lewis representation;
resonance makes the two O–O bonds equivalent in the actual molecule.
"""

import re

_TEXTBOOK_DATIVE = {"O3": True, "H2O2": False, "H2CO": False,
                    "CH2NH": False, "H2O": False, "CO2": False,
                    "NH3": False, "CH4": False, "HCl": False}

def solve(species=("H2O2", "O3", "H2CO", "CH2NH")):
    matches = [item for item in species if _TEXTBOOK_DATIVE[item]]
    assert len(matches) == 1
    return matches[0]


def check(species=("H2O2", "O3", "H2CO", "CH2NH")):
    # Independently count octets for a chain of elemental oxygen atoms:
    # 3(8)-3(6)=6 shared electrons, or three bond pairs distributed as
    # (double, single)/(single, double) over the two O–O links.
    matches = []
    for item in species:
        match = re.fullmatch(r"O(\d+)", item)
        if match and int(match[1]) == 3:
            atoms = int(match[1])
            bond_pairs = (8 * atoms - 6 * atoms) // 2
            if bond_pairs == 3:
                matches.append(item)
    assert len(matches) == 1
    return matches[0]


PARAMS = {"species": ("H2O2", "O3", "H2CO", "CH2NH")}
VARIANTS = [
    {"species": ("O3", "H2O", "CO2", "NH3")},
    {"species": ("CH4", "H2O2", "O3", "HCl")},
    {"species": ("H2CO", "O3", "CO2", "CH2NH")},
]
ANSWER = "O3"
