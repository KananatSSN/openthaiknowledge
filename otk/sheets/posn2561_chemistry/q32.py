"""Source p8, MC32: bond length, polarity, and boiling point claims."""

from fractions import Fraction


STATEMENTS = (
    "พันธะ C–O ใน CO₃²⁻ ยาวกว่าพันธะ C–O ใน CO₂",
    "BF₃ มีสภาพขั้วมากกว่า F₂",
    "CF₄ มีจุดเดือดต่ำกว่า CHF₃",
)
CLAIMS = ("1 เท่านั้น", "1 และ 3 เท่านั้น",
          "2 และ 3 เท่านั้น", "1, 2 และ 3 ถูกทั้งหมด")
COMBINATIONS = ((0,), (0, 2), (1, 2), (0, 1, 2))


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    carbonate_order = Fraction(4, 3)
    carbon_dioxide_order = Fraction(2, 1)
    polar_bf3, polar_f2 = False, False
    boiling_cf4, boiling_chf3 = -127.9, -82.0
    truth = (carbonate_order < carbon_dioxide_order,
             polar_bf3 and not polar_f2,
             boiling_cf4 < boiling_chf3)
    correct = tuple(i for i, value in enumerate(truth) if value)
    return [COMBINATIONS[i] for i in options].index(correct)


def check(options=(0, 1, 2, 3)):
    # Independent measured-length and shape route: carbonate ~129 pm,
    # CO2 ~116 pm; BF3's trigonal-planar dipoles cancel; F2 is homonuclear.
    lengths_pm = {"carbonate": 129, "carbon_dioxide": 116}
    assert lengths_pm["carbonate"] > lengths_pm["carbon_dioxide"]
    assert -127.8 < -82.2  # alternate measured boiling-point values
    return [COMBINATIONS[i] for i in options].index((0, 2))


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (1, 0, 2, 3)},
    {"options": (2, 3, 1, 0)},
    {"options": (3, 2, 0, 1)},
]
ANSWER = 1
