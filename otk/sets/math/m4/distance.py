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

from fractions import Fraction  # noqa: E402

from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m4 import M4 as LEVEL  # noqa: E402


def _nz4(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk4(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk4(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk4(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt4(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk4(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk4(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))

# ── More distance (2026-11): an endpoint from the midpoint, a right triangle's perimeter, a point on the
# x-axis equally far from two points, a missing coordinate from a distance, a centroid, a rectangle's
# diagonal, and a coordinate from the midpoint ──

_TRIPLES4 = ((3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (9, 12, 15), (7, 24, 25))


@question_type("math.endpoint_from_midpoint_m4", display_name={"th": "หาจุดปลายเมื่อรู้จุดกึ่งกลาง"}, level=LEVEL, topic="ระยะทาง")
class EndpointFromMidpointM4(MathType):
    def expr(self, rng: Random):
        ax, ay, mx, my = (rng.randint(-9, 9) for _ in range(4))
        bx, by = 2 * mx - ax, 2 * my - ay
        right = _pt4(bx, by)
        # The midpoint of A and M; M less A; A itself reflected.
        wrongs = [_pt4(Fraction(ax + mx, 2), Fraction(ay + my, 2)), _pt4(mx - ax, my - ay), _pt4(-ax, -ay), _pt4(bx + 1, by)]
        return MathDraw(rf"A{_pt4(ax, ay)}, \; M{_pt4(mx, my)}", right,
                        prompt="M เป็นจุดกึ่งกลางของส่วนของเส้นตรง AB จงหาพิกัดของจุด B", distractors=_tk4(*wrongs, answer=right))


@question_type("math.axis_triangle_perimeter_m4", display_name={"th": "ความยาวรอบรูปสามเหลี่ยมบนแกนพิกัด"}, level=LEVEL,
               topic="ระยะทาง")
class AxisTrianglePerimeterM4(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.choice(_TRIPLES4)
        if rng.random() < 0.5:
            a, b = b, a
        right = a + b + c
        prompt = f"รูปสามเหลี่ยมมีจุดยอดที่ (0, 0), ({a}, 0) และ (0, {b}) มีความยาวรอบรูปกี่หน่วย"
        # The two legs only; the area; the legs and their sum.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk4(a + b, a * b // 2, 2 * (a + b), right + 1, answer=right, lo=1))


@question_type("math.equidistant_on_axis_m4", display_name={"th": "จุดบนแกน x ที่อยู่ห่างจากสองจุดเท่ากัน"}, level=LEVEL,
               topic="ระยะทาง")
class EquidistantOnAxisM4(MathType):
    def expr(self, rng: Random):
        while True:
            a, b, c, d = rng.randint(-8, 8), rng.randint(-8, 8), rng.randint(-8, 8), rng.randint(-8, 8)
            if a != c and (c * c + d * d - a * a - b * b) % (2 * (c - a)) == 0:
                break
        x = (c * c + d * d - a * a - b * b) // (2 * (c - a))
        right = f"({x}, 0)"
        # The midpoint's x; the sign flipped; the y-axis instead.
        wrongs = [_pt4(Fraction(a + c, 2), 0), f"({-x}, 0)", f"(0, {x})", f"({x + 1}, 0)"]
        return MathDraw(rf"A({a}, {b}), \; B({c}, {d})", right, prompt="จุด P บนแกน x อยู่ห่างจาก A และ B เท่ากัน จุด P คือจุดใด",
                        distractors=_tk4(*wrongs, answer=right))


@question_type("math.coordinate_from_distance_m4", display_name={"th": "หาพิกัดที่หายไปจากระยะทาง"}, level=LEVEL,
               topic="ระยะทาง")
class CoordinateFromDistanceM4(MathType):
    def expr(self, rng: Random):
        a, b, c = rng.choice(_TRIPLES4)
        x0, y0 = rng.randint(-6, 6), rng.randint(-6, 6)
        right = x0 + a
        # The negative root; the distance added straight on; the other leg.
        return MathDraw(rf"A({x0}, {y0}), \; B(k, {y0 + b}), \; AB = {c}", str(right),
                        prompt="ถ้า k มากกว่า " + str(x0) + " ค่าของ k เท่ากับเท่าใด",
                        distractors=_nk4(x0 - a, x0 + c, x0 + b, right + 1, answer=right))


@question_type("math.centroid_m4", display_name={"th": "จุดเซนทรอยด์ของรูปสามเหลี่ยม"}, level=LEVEL, topic="ระยะทาง")
class CentroidM4(MathType):
    def expr(self, rng: Random):
        while True:
            pts = [(rng.randint(-9, 9), rng.randint(-9, 9)) for _ in range(3)]
            sx, sy = sum(p[0] for p in pts), sum(p[1] for p in pts)
            if sx % 3 == 0 and sy % 3 == 0:
                break
        right = _pt4(sx // 3, sy // 3)
        # The sums not divided; halved; one vertex.
        wrongs = [_pt4(sx, sy), _pt4(Fraction(sx, 2), Fraction(sy, 2)), _pt4(*pts[0]), _pt4(sx // 3 + 1, sy // 3)]
        verts = r", \; ".join(_pt4(*p) for p in pts)
        return MathDraw(verts, right, prompt="จงหาจุดเซนทรอยด์ (จุดตัดของเส้นมัธยฐาน) ของรูปสามเหลี่ยมที่มีจุดยอดดังนี้",
                        distractors=_tk4(*wrongs, answer=right))


@question_type("math.rectangle_diagonal_coords_m4", display_name={"th": "ความยาวเส้นทแยงมุมจากพิกัด"}, level=LEVEL,
               topic="ระยะทาง")
class RectangleDiagonalCoordsM4(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.choice(_TRIPLES4)
        x0, y0 = rng.randint(-5, 5), rng.randint(-5, 5)
        prompt = (f"รูปสี่เหลี่ยมผืนผ้ามีจุดยอดตรงข้ามกันที่ ({x0}, {y0}) และ ({x0 + a}, {y0 + b}) "
                  "เส้นทแยงมุมยาวกี่หน่วย")
        return MathDraw("", str(c), prompt=prompt, distractors=_nk4(a + b, a * b, 2 * (a + b), c + 1, answer=c, lo=1))


@question_type("math.coordinate_from_midpoint_m4", display_name={"th": "หาพิกัดที่หายไปจากจุดกึ่งกลาง"}, level=LEVEL,
               topic="ระยะทาง")
class CoordinateFromMidpointM4(MathType):
    def expr(self, rng: Random):
        a, b, k, y2 = rng.randint(-9, 9), rng.randint(-9, 9), rng.randint(-9, 9), rng.randint(-9, 9)
        mx, my = Fraction(a + b, 2), Fraction(k + y2, 2)
        # The midpoint's y doubled; the average taken the wrong way; the other end's y.
        return MathDraw(rf"A({a}, k), \; B({b}, {y2}), \; M{_pt4(mx, my)}", str(k),
                        prompt="M เป็นจุดกึ่งกลางของ AB ค่าของ k เท่ากับเท่าใด",
                        distractors=_tk4(frac_tex(2 * my), frac_tex(my - y2), str(y2), str(k + 1), answer=str(k)))
