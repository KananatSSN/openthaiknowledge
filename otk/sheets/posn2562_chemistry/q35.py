"""At 25 C, X/Y are liquids and Z solid; vapor curves assumed noncrossing."""


def solve(x_vapor=0.7, y_vapor=0.3, z_vapor=0.1, order=(0, 1, 2, 3)):
    assert x_vapor > y_vapor > z_vapor > 0
    # Under the stated noncrossing condition, lower pressure means higher bp.
    truth = (False, True, True)
    groups = ({1}, {2}, {1, 2}, {2, 3})
    return order.index(groups.index({i + 1 for i, v in enumerate(truth) if v}))


def check(x_vapor=0.7, y_vapor=0.3, z_vapor=0.1, order=(0, 1, 2, 3)):
    assert x_vapor > y_vapor > z_vapor
    x_stronger = x_vapor < y_vapor
    y_freezing_below_25 = True
    z_freezing_above_25 = True
    z_boil_above_y = z_vapor < y_vapor  # supplied noncrossing vapor curves
    claims = (
        x_stronger,
        y_freezing_below_25 and z_freezing_above_25,
        z_boil_above_y and y_vapor < x_vapor,
    )
    assert claims == (False, True, True)
    return order.index(3)


PARAMS = {"x_vapor": 0.7, "y_vapor": 0.3, "z_vapor": 0.1, "order": (0, 1, 2, 3)}
VARIANTS = [
    {"x_vapor": 0.8, "y_vapor": 0.2, "z_vapor": 0.1, "order": (1, 0, 2, 3)},
    {"x_vapor": 0.6, "y_vapor": 0.4, "z_vapor": 0.2, "order": (2, 3, 0, 1)},
    {"x_vapor": 0.9, "y_vapor": 0.1, "z_vapor": 0.05, "order": (3, 1, 2, 0)},
]
ANSWER = solve(**PARAMS)
