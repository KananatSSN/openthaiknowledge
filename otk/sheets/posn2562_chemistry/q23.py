"""MC23: BF3 incomplete, SF6 and XeF2 expanded — all violate octet."""

OCTET = {"BF3": False, "SF6": False, "XeF2": False,
         "CO": True, "NO": False, "N2O": True,
         "NO2-": True, "O3": True, "I3-": False,
         "N2O3": True, "N2O4": True, "N2H4": True}
GROUPS = (("BF3", "SF6", "XeF2"), ("CO", "NO", "N2O"),
          ("NO2-", "O3", "I3-"), ("N2O3", "N2O4", "N2H4"))


def solve(order=(0, 1, 2, 3)):
    choices = [i for i, group in enumerate(GROUPS)
               if not any(OCTET[molecule] for molecule in group)]
    assert choices == [0]
    return order.index(choices[0])


def check(order=(0, 1, 2, 3)):
    # Count electrons around the unusual central atoms: B 6, S 12, Xe 10.
    first_electrons = (6, 12, 10)
    assert all(count != 8 for count in first_electrons)
    # Each competing group has a conventional-octet counterexample.
    conventional = ("CO", "NO2-", "N2H4")
    assert all(OCTET[x] for x in conventional)
    return order.index(0)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 0, 1)},
            {"order": (3, 1, 2, 0)}]
ANSWER = solve(**PARAMS)
