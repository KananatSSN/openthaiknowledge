"""Source p4, MC11: oxidation states -3 through +5 identify phosphorus."""


def claims(label="D"):
    return (
        f"ธาตุ {label} อยู่ตามปกติในรูป {label}₂",
        f"ธาตุ {label} เป็นแก๊สที่อุณหภูมิห้อง",
        f"ธาตุ {label} มีเลขออกซิเดชันเป็นบวกในออกไซด์",
        f"คลอไรด์ทุกชนิดของ {label} เป็นโมเลกุลมีขั้ว",
    )


def solve(label="D", options=(0, 1, 2, 3)):
    assert label in ("D", "Q", "X", "T")
    assert sorted(options) == [0, 1, 2, 3]
    # P is a solid; white phosphorus is P4. PCl5 is nonpolar as a molecule.
    statements = (False, False, True, False)
    true = [i for i, option in enumerate(options) if statements[option]]
    assert len(true) == 1
    return true[0]


def check(label="D", options=(0, 1, 2, 3)):
    assert label in ("D", "Q", "X", "T")
    evidence = {
        0: "P₄" == "P₂",
        1: "solid" == "gas",
        2: 5 > 0 and 3 > 0,  # P4O10 and P4O6 respectively
        3: "nonpolar" == "polar",  # trigonal-bipyramidal PCl5
    }
    true = [i for i, option in enumerate(options) if evidence[option]]
    assert len(true) == 1
    return true[0]


PARAMS = {"label": "D", "options": (0, 1, 2, 3)}
VARIANTS = [
    {"label": "Q", "options": (2, 0, 1, 3)},
    {"label": "X", "options": (1, 3, 2, 0)},
    {"label": "T", "options": (3, 2, 0, 1)},
]
ANSWER = 2
