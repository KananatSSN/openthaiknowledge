"""Source p4, MC10: warm-water metal Mg and violet iodine identify MgI2.

NIST ASD gives IE3(Mg)=80.1436 eV and IE3(I)=29.570 eV.
"""


IE3_EV = {"Mg": 80.1436, "I": 29.570}
CLAIMS = (
    "สารประกอบ Y เป็น MgI₂ และละลายน้ำได้ดี",
    "สารละลาย X กับสารละลาย Y มีสีทั้งคู่",
    "IE₃ ของ M ต่ำกว่า IE₃ ของ X",
    "Y กับ Na₂SO₄ ให้ตะกอนสีขาว",
)


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    # The observations identify Mg and I2; MgSO4 remains soluble.
    facts = (True, False, IE3_EV["Mg"] < IE3_EV["I"], False)
    true = [i for i, option in enumerate(options) if facts[option]]
    assert len(true) == 1
    return true[0]


def check(options=(0, 1, 2, 3)):
    # Independent route: formulas, visible products, and the IE3 ordering.
    products = {"salt": "MgI₂", "aqueous_iodine": "brown",
                "aqueous_salt": "colorless", "sulfate": "MgSO₄(aq)"}
    statements = (
        products["salt"] == "MgI₂",
        products["aqueous_iodine"] == products["aqueous_salt"],
        not (80 > 30),
        "(s)" in products["sulfate"],
    )
    true = [i for i, option in enumerate(options) if statements[option]]
    assert len(true) == 1
    return true[0]


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (1, 0, 2, 3)},
    {"options": (2, 3, 0, 1)},
    {"options": (3, 2, 1, 0)},
]
ANSWER = 0
