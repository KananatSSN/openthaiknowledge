"""MC19: atomic number 51 is Sb, a metalloid rather than a metal."""


def solve(order=(0, 1, 2, 3)):
    facts = (False, True, True, True)
    return order.index(facts.index(False))


def check(order=(0, 1, 2, 3)):
    # Sb lies on the metalloid staircase in group 15, beneath phosphorus.
    element = {"z": 51, "kind": "metalloid", "group": 15,
               "reacts_cold_water": False, "electronegativity": 2.05}
    phosphorus_en = 2.19
    false_claims = (element["kind"] != "metal",
                    element["reacts_cold_water"],
                    element["electronegativity"] >= phosphorus_en,
                    element["group"] != 15)
    assert false_claims.count(True) == 1
    return order.index(false_claims.index(True))


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 0, 1)},
            {"order": (3, 1, 2, 0)}]
ANSWER = solve(**PARAMS)
