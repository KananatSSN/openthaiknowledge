"""ระยะทาง

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม การวัดและเรขาคณิต 1 ม.4/1

Sets moved here from: math, math_geometry.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, sqrt_tex
from otk.sets._support.math_geometry import _TRIPLES

PROVENANCE = Provenance("original")


@question_type("math.distance_between_points",
               display_name={"th": "ระยะทางระหว่างสองจุด"}, level={"th": "ม.5"},
               topic="ระยะทาง")
class DistanceBetweenPoints(MathType):
    def expr(self, rng: Random):
        x1, y1 = rng.randint(-5, 5), rng.randint(-5, 5)
        while True:
            dx, dy = rng.randint(-6, 6), rng.randint(-6, 6)
            if dx or dy:
                break
        return MathDraw(rf"A({x1}, {y1}), \;\; B({x1 + dx}, {y1 + dy})",
                        sqrt_tex(dx * dx + dy * dy),
                        hint=r"d = \sqrt{(\Delta x)^2 + (\Delta y)^2}",
                        prompt="จงหาระยะทาง AB")


@question_type("math.midpoint", display_name={"th": "จุดกึ่งกลางระหว่างสองจุด"},
               level={"th": "ม.5"}, topic="ระยะทาง")
class Midpoint(MathType):
    def expr(self, rng: Random, lo: int = -12, hi: int = 12):
        # Same parity, so the midpoint has integer coordinates.
        x1, x2 = rng.randint(lo, hi), rng.randint(lo, hi)
        y1, y2 = rng.randint(lo, hi), rng.randint(lo, hi)
        if (x1 + x2) % 2:
            x2 += 1
        if (y1 + y2) % 2:
            y2 += 1
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        return MathDraw(
            f"A({x1}, {y1}), \\; B({x2}, {y2})", f"({mx}, {my})",
            prompt="จงหาพิกัดของจุดกึ่งกลางของ AB",
            distractors=[f"({x2 - x1}, {y2 - y1})", f"({x1 + x2}, {y1 + y2})",
                         f"({my}, {mx})"])


@question_type("math.distance_from_origin", display_name={"th": "ระยะจากจุดกำเนิด"},
               level={"th": "ม.5"}, topic="ระยะทาง")
class DistanceFromOrigin(MathType):
    def expr(self, rng: Random, k_lo: int = 1, k_hi: int = 5):
        a, b, c = rng.choice(_TRIPLES)
        k = rng.randint(k_lo, k_hi)
        x, y = a * k, b * k
        if rng.random() < 0.5:
            x = -x
        if rng.random() < 0.5:
            y = -y
        return MathDraw(f"P({x}, {y})", str(c * k),
                        prompt="จงหาระยะจากจุดกำเนิดถึงจุด P",
                        distractors=[str(abs(x) + abs(y)), str(abs(abs(x) - abs(y))),
                                     str(c * k * 2)])
