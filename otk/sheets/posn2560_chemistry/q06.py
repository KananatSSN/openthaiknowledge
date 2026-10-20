"""Source p4, MC6: cobalt in Co2O3 is Co3+, [Ar]3d6 (choice ค).

Model domain: Mn, Fe, Co and Ni, neutral [Ar]3d^(Z-20)4s2,
and charges 2..4. Ionisation removes 4s before 3d. Oxygen is -2.
Return the exponent of 3d, not a low-spin/high-spin unpaired count.
"""


def solve(atomic=27, metal_count=2, oxygen_count=3):
    charge, remainder = divmod(2 * oxygen_count, metal_count)
    if atomic not in (25, 26, 27, 28) or remainder or charge not in (2, 3, 4):
        raise ValueError("outside the supported integral-charge oxide model")
    return atomic - 18 - charge


def check(atomic=27, metal_count=2, oxygen_count=3):
    # Find oxidation state by electroneutrality, then remove actual electrons
    # from the largest principal quantum number in a neutral occupation list.
    charge = next(q for q in range(2, 5) if metal_count * q - oxygen_count * 2 == 0)
    electrons = [(3, "d")] * (atomic - 20) + [(4, "s")] * 2
    for _ in range(charge):
        electrons.remove(max(electrons))
    assert len(electrons) + 18 == atomic - charge
    return sum(orbital == "d" for _, orbital in electrons)


PARAMS = {"atomic": 27, "metal_count": 2, "oxygen_count": 3}
VARIANTS = [
    {"atomic": 26, "metal_count": 2, "oxygen_count": 3},
    {"atomic": 25, "metal_count": 1, "oxygen_count": 2},
    {"atomic": 28, "metal_count": 1, "oxygen_count": 1},
]
ANSWER = 6
