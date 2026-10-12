"""ข้อ 20 — อัตราส่วนพื้นที่รูปสี่เหลี่ยมด้านขนานต่อพื้นที่วงกลมแนบใน

จงหาค่าต่ำสุดที่เป็นไปได้ของอัตราส่วนระหว่างพื้นที่ของรูปสี่เหลี่ยมด้านขนาน
และพื้นที่ของวงกลมแนบในของรูปสี่เหลี่ยมดังกล่าว

Method: a parallelogram can only have an inscribed circle if it is a rhombus
(opposite sides must sum equally, which for a parallelogram forces all four
equal). With side s and acute angle θ its area is s²·sin θ, and its height
s·sin θ is exactly the circle's diameter, so r = s·sin θ / 2 and

    ratio(θ) = s² sin θ / (π s² sin²θ / 4) = 4 / (π sin θ).

That is smallest where sin θ is largest, i.e. at θ = 90° — the square — giving
4/π ≈ 1.2732. Note the side length cancels: the ratio depends on shape alone.

``check`` builds an actual rhombus from coordinates, measures its area by the
shoelace formula and its inradius as the distance from centre to a side, and
sweeps θ numerically. It never uses the formula above.
"""

from __future__ import annotations

import math

TOL = 1e-6

# theta_deg = 0 is the sheet's own question: minimise over every admissible θ.
# Any other value asks for the ratio of that one rhombus.
PARAMS = {"theta_deg": 0}
ANSWER = 1.2732395447351628           # 4/π
VARIANTS = [
    {"theta_deg": 90},
    {"theta_deg": 30},
    {"theta_deg": 60},
    {"theta_deg": 45},
    {"theta_deg": 120},
]


def ratio(theta_deg: float) -> float:
    """Area of the rhombus over area of its incircle, at acute angle θ."""
    s = math.sin(math.radians(theta_deg))
    if s <= 0:
        raise ValueError("θ must be strictly between 0° and 180°")
    return 4 / (math.pi * s)


def solve(theta_deg=0):
    """The minimum ratio (θ = 0), or the ratio at one given angle."""
    return 4 / math.pi if theta_deg == 0 else ratio(theta_deg)


def _built_ratio(theta_deg: float, side: float = 1.7) -> float:
    """Same ratio, from an explicitly constructed rhombus."""
    t = math.radians(theta_deg)
    pts = [(0.0, 0.0), (side, 0.0),
           (side + side * math.cos(t), side * math.sin(t)),
           (side * math.cos(t), side * math.sin(t))]
    area = abs(sum(pts[i][0] * pts[(i + 1) % 4][1] - pts[(i + 1) % 4][0] * pts[i][1]
                   for i in range(4))) / 2
    centre = (sum(p[0] for p in pts) / 4, sum(p[1] for p in pts) / 4)
    # inradius = distance from the centre to the side lying on the x-axis
    r = abs(centre[1])
    return area / (math.pi * r * r)


def check(theta_deg=0):
    """Independent: construct the rhombus; for the minimum, sweep θ."""
    if theta_deg != 0:
        return _built_ratio(theta_deg)
    best = min(_built_ratio(1 + 178 * i / 20000) for i in range(20001))
    return best
