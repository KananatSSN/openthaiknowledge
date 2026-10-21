"""Three precipitates: CaCO3, BaSO4 and SrHPO4."""

REACTIONS = (
    "Ca2+ + CO3^2- -> CaCO3(s)",
    "Ba2+ + SO4^2- -> BaSO4(s)",
    "Sr2+ + HPO4^2- -> SrHPO4(s)",
)


def solve(order=(0, 1, 2, 3)):
    precipitating = {1, 3, 4}
    choices = ({1, 2, 3}, {1, 3, 4}, {1, 4, 5}, {2, 3, 5})
    return order.index(choices.index(precipitating))


def check(order=(0, 1, 2, 3)):
    # Chlorides/nitrates soluble; carbonate, sulfate and SrHPO4 precipitate.
    insoluble = ("CaCO3", "BaSO4", "SrHPO4")
    assert len(REACTIONS) == len(insoluble) == 3
    return order.index(1)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 0, 1)}, {"order": (3, 1, 2, 0)}]

ANSWER = solve(**PARAMS)
