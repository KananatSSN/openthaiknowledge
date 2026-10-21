"""Source p8, MC28: identify the false NH₄⁺ bonding claim."""


CLAIMS = (
    "NH₄⁺ มีรูปร่างทรงสี่หน้า",
    "พันธะ N–H ทั้งสี่มีขั้ว",
    "อะตอมไนโตรเจนที่เป็นอะตอมกลางไม่มีอิเล็กตรอนคู่โดดเดี่ยว",
    "พันธะ N–H หนึ่งพันธะยาวกว่าอีกสามพันธะ",
)


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    # Four identical H ligands around N give four equivalent N–H bonds.
    bonds, lone_pairs = 4, 0
    true = (bonds == 4 and lone_pairs == 0,
            True, lone_pairs == 0, False)
    false = [i for i, option in enumerate(options) if not true[option]]
    assert len(false) == 1
    return false[0]


def check(options=(0, 1, 2, 3)):
    # Independent Lewis construction: NH3 donates its lone pair to H+;
    # four equivalent tetrahedral sites have the same N-H distance.
    valence_electrons = 5 + 4 - 1
    assert valence_electrons == 8
    tetrahedron = ((1, 1, 1), (1, -1, -1),
                   (-1, 1, -1), (-1, -1, 1))
    squared_bond_lengths = {sum(coordinate * coordinate for coordinate in site)
                            for site in tetrahedron}
    assert squared_bond_lengths == {3}
    return options.index(3)


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (3, 0, 1, 2)},
    {"options": (1, 3, 2, 0)},
    {"options": (2, 1, 0, 3)},
]
ANSWER = 3
