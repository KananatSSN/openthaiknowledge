"""Source p13, MC56: water cohesion versus adhesion to surfaces."""


SURFACES = {
    "lotus": "ใบบัว",
    "tissue": "กระดาษชำระ",
    "glass": "กระจกสะอาดที่ไม่เคลือบสารกันน้ำ",
}


def solve(order=("lotus", "tissue", "glass")):
    assert sorted(order) == sorted(SURFACES)
    return order.index("lotus") + 1


def check(order=("lotus", "tissue", "glass")):
    wets = {"lotus": False, "tissue": True, "glass": True}
    beading = [number for number, surface in enumerate(order, 1) if not wets[surface]]
    assert len(beading) == 1
    return beading[0]


PARAMS = {"order": ("lotus", "tissue", "glass")}
VARIANTS = [
    {"order": ("glass", "lotus", "tissue")},
    {"order": ("tissue", "glass", "lotus")},
    {"order": ("tissue", "lotus", "glass")},
]
ANSWER = 1
