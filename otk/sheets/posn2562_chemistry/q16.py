"""MC16: joining two light deuterium nuclei is fusion."""


def solve(order=(0, 1, 2, 3)):
    # The other options are Al+He transmutation, beta decay, and U fission.
    reactants = ((2, 2), (27, 4), (214,), (235, 1))
    product_largest = (3, 30, 214, 144)
    fusion = [i for i, masses in enumerate(reactants)
              if len(masses) == 2 and all(m <= 4 for m in masses)
              and product_largest[i] > max(masses)]
    assert fusion == [0]
    return order.index(fusion[0])


def check(order=(0, 1, 2, 3)):
    # Verify the first equation conserves A/Z: 2H+2H -> 3He+n.
    mass_ok = 2 + 2 == 3 + 1
    charge_ok = 1 + 1 == 2 + 0
    candidates = (mass_ok and charge_ok, False, False, False)
    assert candidates.count(True) == 1
    return order.index(candidates.index(True))


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 0, 1)},
            {"order": (3, 1, 2, 0)}]
ANSWER = solve(**PARAMS)
