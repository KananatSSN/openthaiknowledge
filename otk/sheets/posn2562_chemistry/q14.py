"""MC14: Cu is [Ar]3d10 4s1; Cu(II) is 3d9, each with one unpaired electron."""


def solve(order=(0, 1, 2, 3)):
    neutral_d, neutral_s = 10, 1
    oxide_charge = 2
    ion_d = neutral_d - (oxide_charge - neutral_s)
    counts = (neutral_s, 1 if ion_d % 2 else 0)
    choices = ((1, 0), (1, 1), (0, 0), (1, 3))
    return order.index(choices.index(counts))


def check(order=(0, 1, 2, 3)):
    # Count singly occupied orbitals directly from occupation lists.
    neutral = [2] * 5 + [1]
    ion = [2] * 4 + [1]
    observed = (neutral.count(1), ion.count(1))
    choices = ((1, 0), (1, 1), (0, 0), (1, 3))
    return order.index(choices.index(observed))


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 1, 0)},
            {"order": (3, 1, 0, 2)}]
ANSWER = solve(**PARAMS)
