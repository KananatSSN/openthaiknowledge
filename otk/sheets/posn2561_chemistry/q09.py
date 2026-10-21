"""Source p4, MC9: SO3 makes acid and Na2O makes base in water."""


PAIRS = (("BeO", "N₂O₅"), ("SiO₂", "CaO"),
         ("Cl₂O₇", "Al₂O₃"), ("SO₃", "Na₂O"))
ACID_IN_WATER = {"N₂O₅", "Cl₂O₇", "SO₃"}
BASE_IN_WATER = {"CaO", "Na₂O"}


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    true = [i for i, pair_index in enumerate(options)
            if PAIRS[pair_index][0] in ACID_IN_WATER
            and PAIRS[pair_index][1] in BASE_IN_WATER]
    assert len(true) == 1
    return true[0]


def check(options=(0, 1, 2, 3)):
    # Independently classify the reaction products and insoluble oxides.
    products = {"BeO": None, "N₂O₅": "HNO₃", "SiO₂": None,
                "CaO": "Ca(OH)₂", "Cl₂O₇": "HClO₄", "Al₂O₃": None,
                "SO₃": "H₂SO₄", "Na₂O": "NaOH"}
    acidic = {"HNO₃", "HClO₄", "H₂SO₄"}
    basic = {"Ca(OH)₂", "NaOH"}
    true = [i for i, pair_index in enumerate(options)
            if products[PAIRS[pair_index][0]] in acidic
            and products[PAIRS[pair_index][1]] in basic]
    assert len(true) == 1
    return true[0]


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (3, 0, 1, 2)},
    {"options": (1, 3, 2, 0)},
    {"options": (2, 1, 0, 3)},
]
ANSWER = 3
