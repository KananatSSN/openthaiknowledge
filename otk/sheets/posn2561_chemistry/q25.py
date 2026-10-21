"""Source p7, MC25: solvent extraction table gives a polarity trend.

The source table reads hexane A 90/B 10; chloroform B 80/C 20;
ethanol C 70/D 30 (mass percentages within each extract). These are
qualitative affinities, not molecular structures. The adaptation explicitly
asks for the likely trend, rather than asserting an exact polarity class.
"""


EXTRACTS = (
    ("เฮกเซน", (("A", 90), ("B", 10))),
    ("คลอโรฟอร์ม", (("B", 80), ("C", 20))),
    ("เอทานอล", (("C", 70), ("D", 30))),
)
STATEMENTS = (
    "A และ B ต้องเป็นสารไม่มีขั้วทั้งคู่ ส่วน C และ D ต้องเป็นสารมีขั้ว",
    "C มีแนวโน้มมีขั้วมากกว่า B",
    "D อาจมีแรงระหว่างขั้ว และถ้ามีหมู่ที่เหมาะสมอาจเกิดพันธะไฮโดรเจน",
)
CLAIMS = ("1 เท่านั้น", "2 เท่านั้น", "2 และ 3 เท่านั้น", "1, 2 และ 3 ทั้งหมดถูกต้อง")
COMBINATIONS = ((0,), (1,), (1, 2), (0, 1, 2))


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    # Solvent polarity increases hexane < chloroform < ethanol. The dominant
    # extraction for B is chloroform and for C ethanol. This does not prove
    # that B is strictly nonpolar or that D has an H-bond donor.
    dominant = {substance: solvent_index for substance in "ABCD"
                for solvent_index, (_, composition) in enumerate(EXTRACTS)
                if any(name == substance and fraction >= 50
                       for name, fraction in composition)}
    assert dominant == {"A": 0, "B": 1, "C": 2}
    truth = (False, dominant["C"] > dominant["B"], True)
    correct = tuple(i for i, value in enumerate(truth) if value)
    return [COMBINATIONS[i] for i in options].index(correct)


def check(options=(0, 1, 2, 3)):
    # Independent reading: B occurs mainly in the middle-polarity extract,
    # C mainly in the most polar extract; molecular structure is unknown.
    most_abundant = [max(composition, key=lambda pair: pair[1])[0]
                     for _, composition in EXTRACTS]
    assert most_abundant == ["A", "B", "C"]
    assert EXTRACTS[2][1][-1] == ("D", 30)
    return options.index(2)


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (2, 0, 1, 3)},
    {"options": (1, 3, 2, 0)},
    {"options": (3, 2, 0, 1)},
]
ANSWER = 2
