"""Source p4, MC5: A=Mg (Z=12), E=P (Z=15), J=As (Z=33).

The true choice ง compares Mg2+ and P3-. Mg2+ has ten electrons in two
occupied shells; P3- has eighteen in three. The adaptation compares ion
radii only when their outer occupied shell differs, avoiding a false rule
for ions with the same shell count.
"""


def _shell(electrons):
    if electrons <= 0 or electrons > 36:
        raise ValueError("electron count outside supported range")
    return next(n for n, capacity in enumerate((2, 10, 18, 36), 1)
                if electrons <= capacity)


def solve(first_atomic=12, first_charge=2, second_atomic=15, second_charge=-3):
    first = _shell(first_atomic - first_charge)
    second = _shell(second_atomic - second_charge)
    if first == second:
        raise ValueError("equal-shell ionic radii need more information")
    return "first" if first < second else "second"


def check(first_atomic=12, first_charge=2, second_atomic=15, second_charge=-3):
    # Populate actual orbitals in energy order and inspect the maximum n.
    orbitals = ((1, 2), (2, 2), (2, 6), (3, 2), (3, 6), (4, 2), (3, 10), (4, 6))

    def outer(atomic, charge):
        remaining = atomic - charge
        occupied = []
        for principal, capacity in orbitals:
            take = min(remaining, capacity)
            occupied.extend([principal] * take)
            remaining -= take
            if remaining == 0:
                break
        return max(occupied)

    radii = (outer(first_atomic, first_charge), outer(second_atomic, second_charge))
    assert radii[0] != radii[1]
    return "first" if radii[0] < radii[1] else "second"


PARAMS = {"first_atomic": 12, "first_charge": 2, "second_atomic": 15, "second_charge": -3}
VARIANTS = [
    {"first_atomic": 15, "first_charge": -3, "second_atomic": 12, "second_charge": 2},
    {"first_atomic": 11, "first_charge": 1, "second_atomic": 17, "second_charge": -1},
    {"first_atomic": 20, "first_charge": 2, "second_atomic": 33, "second_charge": -3},
]
ANSWER = "first"
