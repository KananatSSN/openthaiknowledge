"""Source pp6–7, MC22: compare molecular CS₂ with network SiO₂."""


CLAIMS = (
    "A มีแรงยึดเหนี่ยวระหว่างโมเลกุลแบบขั้ว–ขั้ว",
    "A มีจุดหลอมเหลวและจุดเดือดสูงกว่า B",
    "B ไม่ละลายน้ำและมีจุดหลอมเหลวกับจุดเดือดสูง",
    "B ละลายได้ดีในเฮกเซน",
)


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    # Z=6,16 yield linear CS2; Z=14,8 yield covalent-network SiO2.
    properties = {"A": ("molecular", False, False),
                  "B": ("network", False, True)}
    valid = (properties["A"][1],
             properties["A"][2] and not properties["B"][2],
             properties["B"][2] and not properties["B"][1],
             properties["B"][1])
    matches = [i for i, option in enumerate(options) if valid[option]]
    assert len(matches) == 1
    return matches[0]


def check(options=(0, 1, 2, 3)):
    # Independent structural check: CS2's two opposing C=S bond dipoles
    # cancel; SiO2 is an extended Si–O framework, not discrete molecules.
    descriptions = (False, False, True, False)
    assert descriptions.count(True) == 1
    return [descriptions[i] for i in options].index(True)


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (2, 0, 1, 3)},
    {"options": (1, 3, 2, 0)},
    {"options": (3, 2, 0, 1)},
]
ANSWER = 2
