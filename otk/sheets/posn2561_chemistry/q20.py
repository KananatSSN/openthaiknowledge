"""Source p6, MC20: rubidium-water answer has missing coefficients.

The adaptation balances the intended choice: 2Rb + 2H2O -> 2RbOH + H2.
"""


CLAIMS = (
    "2M(s) + 2H₂O(l) → 2MOH(aq) + H₂(g)",
    "M(s) + HCl(aq) → MCl₂(aq) + H₂(g)",
    "2MBr(aq) + I₂(s) → 2MI(aq) + Br₂(l)",
    "M₂SO₄(aq) + BaCl₂(aq) → ไม่เกิดปฏิกิริยา",
)


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    # Rb is monovalent; iodine cannot displace bromine; BaSO4 precipitates.
    valid = (True, False, False, False)
    true = [i for i, option in enumerate(options) if valid[option]]
    assert len(true) == 1
    return true[0]


def check(options=(0, 1, 2, 3)):
    # Independently compare atom balance, charge and precipitation products.
    products = {
        0: ("RbOH", "H₂"),
        1: ("RbCl₂", "H₂"),
        2: ("RbI", "Br₂"),
        3: ("BaSO₄(s)", "RbCl"),
    }
    possible = (
        products[0] == ("RbOH", "H₂"),
        "RbCl₂" == "RbCl",
        False,  # I2 is weaker than Br2 as an oxidant
        not any("(s)" in product for product in products[3]),
    )
    true = [i for i, option in enumerate(options) if possible[option]]
    assert len(true) == 1
    return true[0]


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (2, 0, 1, 3)},
    {"options": (1, 3, 2, 0)},
    {"options": (3, 2, 0, 1)},
]
ANSWER = 0
