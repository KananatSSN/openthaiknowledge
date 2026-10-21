"""Source p7, MC23: VSEPR shape and molecular polarity."""


STATEMENTS = (
    "SbCl₅ มีพันธะมีขั้ว แต่โมเลกุลไม่มีขั้วในสถานะแก๊ส",
    "SiH₄ มีรูปทรงสี่หน้าและโมเลกุลมีขั้ว",
    "TeF₆ มีรูปทรงแปดหน้าและ Te ไม่มีอิเล็กตรอนคู่โดดเดี่ยว",
)
CLAIMS = ("1 และ 3 เท่านั้น", "1 และ 2 เท่านั้น",
          "2 และ 3 เท่านั้น", "1, 2 และ 3")
COMBINATIONS = ((0, 2), (0, 1), (1, 2), (0, 1, 2))


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    # AX5 trigonal bipyramidal and AX6 octahedral are symmetric;
    # tetrahedral SiH4 is also symmetric, so statement 2 is false.
    true_statements = {0, 2}
    matches = [i for i, option in enumerate(options)
               if set(COMBINATIONS[option]) == true_statements]
    assert len(matches) == 1
    return matches[0]


def check(options=(0, 1, 2, 3)):
    # Independently count bonding domains and lone pairs on the centers.
    domains = {"SbCl₅": (5, 0), "SiH₄": (4, 0), "TeF₆": (6, 0)}
    assert domains["SbCl₅"] == (5, 0)
    assert domains["SiH₄"] == (4, 0)
    assert domains["TeF₆"] == (6, 0)
    truth = (True, False, True)
    return [tuple(i for i, value in enumerate(truth) if value)
            == COMBINATIONS[option] for option in options].index(True)


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (1, 0, 2, 3)},
    {"options": (2, 3, 1, 0)},
    {"options": (3, 2, 0, 1)},
]
ANSWER = 0
