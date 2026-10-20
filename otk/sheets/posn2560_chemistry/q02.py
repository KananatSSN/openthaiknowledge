"""Source p3, MC2: the false Ts conjecture is 'oxidation state only -1'.

Ts (Z=117) is predicted to have oxidation states -1, +1, +3 and +5; these
are predictions, not measured chemical properties. Its 7p5 ground-state
occupation has one unpaired electron. The adaptation supplies a model's
possible oxidation states explicitly and asks which claim it contradicts.
"""


def solve(states=(-1, 1, 3, 5), outer_p=5):
    if outer_p != 5 or -1 not in states or not any(s > 0 for s in states):
        raise ValueError("requires a group-17 p5 model with positive states")
    return "only_minus_one"


def check(states=(-1, 1, 3, 5), outer_p=5):
    # Fill three p orbitals by Hund's rule, then evaluate each claim.
    occupancy = [0, 0, 0]
    for i in range(outer_p):
        occupancy[i % 3] += 1
    unpaired = sum(value == 1 for value in occupancy)
    claims = {
        "has_minus_one": -1 in states,
        "has_positive": any(value > 0 for value in states),
        "only_minus_one": set(states) == {-1},
        "one_unpaired": unpaired == 1,
    }
    false_claims = [name for name, holds in claims.items() if not holds]
    assert len(false_claims) == 1
    return false_claims[0]


PARAMS = {"states": (-1, 1, 3, 5), "outer_p": 5}
VARIANTS = [
    {"states": (-1, 1), "outer_p": 5},
    {"states": (-1, 1, 3), "outer_p": 5},
    {"states": (-1, 1, 5, 7), "outer_p": 5},
]
ANSWER = "only_minus_one"
