"""MC30: CCl4 vapour pressure exceeds water; SF4 boils above SF6."""


def solve(order=(0, 1, 2, 3)):
    ccl4_mm, water_mm = 91.3, 17.5
    sf4_bp, sf6_bp = -38, -63.8
    so2_soluble = True
    claims = (ccl4_mm < water_mm, sf4_bp > sf6_bp, not so2_soluble)
    true = tuple(i for i, value in enumerate(claims, 1) if value)
    groups = ((1,), (2,), (3,), (1, 2))
    return order.index(groups.index(true))


def check(order=(0, 1, 2, 3)):
    # At 20°C carbon tetrachloride is much more volatile than water.
    higher_vapor_pressure = "CCl4"
    # SF6 normal boiling is below -60°C while SF4's is near -40°C.
    boiling_order = -40 > -60
    # Dissolved SO2 makes sulfurous-acid-containing water.
    sulfur_dioxide_dissolves = True
    valid = (higher_vapor_pressure == "water", boiling_order,
             not sulfur_dioxide_dissolves)
    assert valid == (False, True, False)
    return order.index(1)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (1, 0, 2, 3)}, {"order": (2, 3, 1, 0)},
            {"order": (3, 1, 0, 2)}]
ANSWER = solve(**PARAMS)
