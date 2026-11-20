"""Source p9, MC24: XeF2 has three central-atom lone pairs (choice ข)."""

_LONE_PAIRS = {
    "NH3": 1, "XeF2": 3, "NO2-": 1, "SO3^2-": 1,
    "I3-": 3, "XeF4": 2, "ClF3": 2, "SF4": 1,
}

# AX_mE_n from independently drawn Lewis structures, where E is the
# number of lone pairs on the indicated central atom.
_AXE = {
    "NH3": (3, 1), "XeF2": (2, 3), "NO2-": (2, 1), "SO3^2-": (3, 1),
    "I3-": (2, 3), "XeF4": (4, 2), "ClF3": (3, 2), "SF4": (4, 1),
}


def solve(species=("NH3", "XeF2", "NO2-", "SO3^2-")):
    highest = max(_LONE_PAIRS[item] for item in species)
    matches = [item for item in species if _LONE_PAIRS[item] == highest]
    assert len(matches) == 1
    return matches[0]


def check(species=("NH3", "XeF2", "NO2-", "SO3^2-")):
    highest = max(_AXE[item][1] for item in species)
    matches = [item for item in species if _AXE[item][1] == highest]
    assert len(matches) == 1
    return matches[0]


PARAMS = {"species": ("NH3", "XeF2", "NO2-", "SO3^2-")}
VARIANTS = [
    {"species": ("I3-", "XeF4", "NH3", "SO3^2-")},
    {"species": ("XeF2", "ClF3", "SF4", "NO2-")},
    {"species": ("XeF4", "NH3", "NO2-", "SO3^2-")},
]
ANSWER = "XeF2"
