"""Source pp7–8, MC26: fractional-distillation order of three compounds."""


BOILING_C = {"บิวเทน": -0.5, "ไดเอทิลอีเทอร์": 34.6, "เอทานอล": 78.4}
ORDERS = (
    ("เอทานอล", "ไดเอทิลอีเทอร์", "บิวเทน"),
    ("ไดเอทิลอีเทอร์", "บิวเทน", "เอทานอล"),
    ("บิวเทน", "ไดเอทิลอีเทอร์", "เอทานอล"),
    ("บิวเทน", "เอทานอล", "ไดเอทิลอีเทอร์"),
)


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    first_to_last = tuple(sorted(BOILING_C, key=BOILING_C.get))
    return [ORDERS[i] for i in options].index(first_to_last)


def check(options=(0, 1, 2, 3)):
    # Independently apply intermolecular-force trend: butane has only
    # dispersion; ether has a permanent dipole; ethanol H-bonds.
    force_rank = {"บิวเทน": 0, "ไดเอทิลอีเทอร์": 1, "เอทานอล": 2}
    valid = [i for i, option in enumerate(options)
             if [force_rank[name] for name in ORDERS[option]] == [0, 1, 2]]
    assert len(valid) == 1
    return valid[0]


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (2, 0, 1, 3)},
    {"options": (1, 3, 2, 0)},
    {"options": (3, 2, 0, 1)},
]
ANSWER = 2
