"""Source p6, MC12: X2+ and Y- are isoelectronic with Ar (18 electrons).

Thus X is Ca (group 2, period 4), Y is Cl (old VIIA/group 7,
period 3): choice ข. The adaptation keeps the source's short group 7
notation rather than modern group 17.
"""

_NOBLE_PERIOD = {10: 2, 18: 3, 36: 4, 54: 5}


def solve(noble_electrons=18):
    if noble_electrons not in _NOBLE_PERIOD:
        raise ValueError("supported noble-gas electron counts only")
    period = _NOBLE_PERIOD[noble_electrons]
    return 2, period + 1, 7, period


def check(noble_electrons=18):
    # Independently identify the neutral elements from their Z values and
    # look up their actual table positions (old main-group numbering).
    locations = {
        9: (7, 2), 12: (2, 3),
        17: (7, 3), 20: (2, 4),
        35: (7, 4), 38: (2, 5),
        53: (7, 5), 56: (2, 6),
    }
    return (*locations[noble_electrons + 2], *locations[noble_electrons - 1])


PARAMS = {"noble_electrons": 18}
VARIANTS = [
    {"noble_electrons": 10},
    {"noble_electrons": 36},
    {"noble_electrons": 54},
]
ANSWER = (2, 4, 7, 3)
