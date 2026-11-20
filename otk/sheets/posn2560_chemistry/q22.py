"""Source p8, MC22: BF4- and POCl3 are both tetrahedral (choice ง)."""

_SHAPE = {
    "BF4-": "tetrahedral", "POCl3": "tetrahedral",
    "ICl4-": "square_planar", "XeF4": "square_planar",
    "TeCl4": "seesaw", "SF4": "seesaw",
    "NH3": "trigonal_pyramidal", "PCl3": "trigonal_pyramidal",
}

# (bonding domains, central-atom lone pairs), from Lewis structures.
_AXE = {
    "BF4-": (4, 0), "POCl3": (4, 0),
    "ICl4-": (4, 2), "XeF4": (4, 2),
    "TeCl4": (4, 1), "SF4": (4, 1),
    "NH3": (3, 1), "PCl3": (3, 1),
}


def solve(pairs=(("BF4-", "ICl4-"), ("TeCl4", "POCl3"),
                 ("ICl4-", "TeCl4"), ("BF4-", "POCl3"))):
    matches = [pair for pair in pairs if _SHAPE[pair[0]] == _SHAPE[pair[1]]]
    assert len(matches) == 1
    return matches[0]


def check(pairs=(("BF4-", "ICl4-"), ("TeCl4", "POCl3"),
                 ("ICl4-", "TeCl4"), ("BF4-", "POCl3"))):
    # Independent AX_mE_n classifications: all supported comparisons
    # have distinct molecular shapes when their AXE signatures differ.
    matches = [pair for pair in pairs if _AXE[pair[0]] == _AXE[pair[1]]]
    assert len(matches) == 1
    return matches[0]


_WRONG = (("BF4-", "ICl4-"), ("TeCl4", "POCl3"),
          ("ICl4-", "TeCl4"))
PARAMS = {"pairs": (*_WRONG, ("BF4-", "POCl3"))}
VARIANTS = [
    {"pairs": (*_WRONG, ("ICl4-", "XeF4"))},
    {"pairs": (*_WRONG, ("TeCl4", "SF4"))},
    {"pairs": (*_WRONG, ("NH3", "PCl3"))},
]
ANSWER = ("BF4-", "POCl3")
