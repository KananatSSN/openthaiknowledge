"""เรขาคณิตวิเคราะห์

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม การวัดและเรขาคณิต 1 ม.4/1

Sets moved here from: math, math_geometry, math_m4.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, frac_tex
from otk.sets._support.math_m4 import M4

PROVENANCE = Provenance("original")


@question_type("math.slope_between_points",
               display_name={"th": "ความชันของเส้นตรงจากสองจุด"}, level={"th": "ม.4"},
               topic="เรขาคณิตวิเคราะห์")
class SlopeBetweenPoints(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        x1, y1 = rng.randint(-5, 5), rng.randint(-5, 5)
        while True:
            dx, dy = rng.randint(-6, 6), rng.randint(-6, 6)
            if dx:
                break
        x2, y2 = x1 + dx, y1 + dy
        m = Fraction(dy, dx)
        wrong = [frac_tex(-m), frac_tex(Fraction(dx, dy)) if dy else str(dx),
                 frac_tex(Fraction(dy + dx, dx))]
        return MathDraw(rf"({x1}, {y1}), \;\; ({x2}, {y2})", frac_tex(m),
                        prompt="จงหาความชันของเส้นตรงที่ผ่านจุดทั้งสอง",
                        distractors=wrong)


@question_type("math.slope_from_equation", display_name={"th": "ความชันจากสมการเส้นตรง"},
               level={"th": "ม.4"}, topic="เรขาคณิตวิเคราะห์")
class SlopeFromEquation(MathType):
    """Ax + By = C rearranged: the slope is −A/B, and the minus sign is the
    single most common slip."""

    def expr(self, rng: Random, coef_hi: int = 9):
        a = rng.choice([n for n in range(-coef_hi, coef_hi + 1) if n])
        b = rng.choice([n for n in range(-coef_hi, coef_hi + 1) if n])
        c = rng.randint(-12, 12)
        slope = Fraction(-a, b)
        lhs = f"{a}x {'+' if b >= 0 else '-'} {abs(b)}y"
        return MathDraw(f"{lhs} = {c}", frac_tex(slope),
                        prompt="จงหาความชันของเส้นตรงนี้",
                        distractors=[frac_tex(-slope), frac_tex(Fraction(b, a)),
                                     frac_tex(Fraction(a, b))])


@question_type("math.parallel_perpendicular_slope",
               display_name={"th": "ความชันของเส้นขนานและเส้นตั้งฉาก"},
               level={"th": "ม.4"}, topic="เรขาคณิตวิเคราะห์")
class ParallelPerpendicularSlope(MathType):
    def expr(self, rng: Random, num_hi: int = 9, den_hi: int = 9):
        m = Fraction(rng.choice([n for n in range(-num_hi, num_hi + 1) if n]),
                     rng.randint(1, den_hi))
        if rng.random() < 0.5:
            kind, answer = "ขนานกับ", m
        else:
            kind, answer = "ตั้งฉากกับ", -1 / m
        return MathDraw(
            rf"m = {frac_tex(m)}", frac_tex(answer),
            prompt=f"เส้นตรงที่{kind}เส้นตรงซึ่งมีความชันนี้ มีความชันเท่าใด",
            distractors=[frac_tex(m), frac_tex(-m), frac_tex(1 / m),
                         frac_tex(-1 / m)])


@question_type("math.triangle_area_coordinates_m4",
               display_name={"th": "พื้นที่รูปสามเหลี่ยมจากพิกัดจุดยอด"},
               level=M4, topic="เรขาคณิตวิเคราะห์")
class TriangleAreaCoordinatesM4(MathType):
    def expr(self, rng: Random):
        while True:
            pts = [(rng.randint(-6, 6), rng.randint(-6, 6)) for _ in range(3)]
            (x1, y1), (x2, y2), (x3, y3) = pts
            twice = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            if twice and twice % 2 == 0:
                break
        area = twice // 2
        tex = r",\ ".join(f"({x}, {y})" for x, y in pts)
        return MathDraw(tex, str(area), prompt="จงหาพื้นที่ของรูปสามเหลี่ยมที่มีจุดยอดดังนี้",
                        # The determinant without the half, and one sign slip.
                        distractors=_story.keep(twice, area + 2, area * 4 if area < 50 else area - 2,
                                                answer=area, lo=1))


from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import question_type  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.kit.math_problems import poly_tex  # noqa: E402
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

# ── More analytic geometry (2026-11): three points on a line, the angle a slope makes, a parallelogram's area
# from coordinates, a slope from the intercepts, parallel lines, and perpendicular lines ──


@question_type("math.collinear_k_m4", display_name={"th": "หาค่า k ที่ทำให้สามจุดอยู่บนเส้นตรงเดียวกัน"}, level=LEVEL,
               topic="เรขาคณิตวิเคราะห์")
class CollinearKM4(MathType):
    def expr(self, rng: Random):
        a, m = rng.randint(-9, 9), _nz4(rng, 1, 5)
        d = rng.randint(2, 4)
        b = a + m
        k = a + m * d
        # Only one step taken; the step doubled; the sign of the slope flipped.
        return MathDraw(rf"(0, {a}), \; (1, {b}), \; ({d}, k)", str(k), prompt="ถ้าสามจุดนี้อยู่บนเส้นตรงเดียวกัน ค่าของ k เท่ากับเท่าใด",
                        distractors=_nk4(b, a + 2 * m * d, a - m * d, k + 1, answer=k))


@question_type("math.slope_angle_m4", display_name={"th": "มุมที่เส้นตรงทำกับแกน x"}, level=LEVEL, topic="เรขาคณิตวิเคราะห์")
class SlopeAngleM4(ConceptBankType):
    ITEMS = [
        Concept("เส้นตรงที่มีความชัน 1 ทำมุมกับแกน x ทางบวกกี่องศา", "45°", ("30°", "60°", "90°")),
        Concept("เส้นตรงที่มีความชัน √3 ทำมุมกับแกน x ทางบวกกี่องศา", "60°", ("30°", "45°", "120°")),
        Concept("เส้นตรงที่มีความชัน −1 ทำมุมกับแกน x ทางบวกกี่องศา", "135°", ("45°", "−45°", "90°")),
        Concept("เส้นตรงที่มีความชัน 1/√3 ทำมุมกับแกน x ทางบวกกี่องศา", "30°", ("60°", "45°", "15°")),
        Concept("เส้นตรงที่ขนานกับแกน y มีความชันเป็นอย่างไร", "หาค่าไม่ได้", ("0", "1", "−1")),
    ]


@question_type("math.parallelogram_area_coords_m4", display_name={"th": "พื้นที่สี่เหลี่ยมด้านขนานจากพิกัด"}, level=LEVEL,
               topic="เรขาคณิตวิเคราะห์")
class ParallelogramAreaCoordsM4(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.randint(2, 9), rng.randint(1, 6), rng.randint(2, 9)
        right = a * c
        prompt = (f"รูปสี่เหลี่ยมด้านขนานมีจุดยอดที่ (0, 0), ({a}, 0), ({a + b}, {c}) และ ({b}, {c}) "
                  "มีพื้นที่กี่ตารางหน่วย")
        # The slanted side used as the height; halved; the sides added.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk4((a + b) * c, a * c // 2 if a * c % 2 == 0 else a + c, 2 * (a + c), a * (b + c),
                                         answer=right, lo=1))


@question_type("math.slope_from_intercepts_m4", display_name={"th": "ความชันจากจุดตัดแกน"}, level=LEVEL,
               topic="เรขาคณิตวิเคราะห์")
class SlopeFromInterceptsM4(MathType):
    def expr(self, rng: Random):
        a, b = _nz4(rng, 1, 9), _nz4(rng, 1, 9)
        right = Fraction(-b, a)
        return MathDraw(rf"({a}, 0), \; (0, {b})", frac_tex(right), prompt="เส้นตรงตัดแกน x และแกน y ที่จุดเหล่านี้ ความชันเท่ากับเท่าใด",
                        distractors=_fk4(Fraction(b, a), Fraction(-a, b), Fraction(a, b), right + 1, answer=right))


@question_type("math.parallel_lines_k_m4", display_name={"th": "ค่า k ที่ทำให้เส้นตรงสองเส้นขนานกัน"}, level=LEVEL,
               topic="เรขาคณิตวิเคราะห์")
class ParallelLinesKM4(MathType):
    def expr(self, rng: Random):
        a = rng.choice((1, 2, 3, 6))
        b, c = rng.randint(1, 9), rng.randint(-9, 9)
        k = 6 // a * b
        # The sign flipped; the ratio upside down; the product.
        return MathDraw(rf"{a}x + {b}y = {c}, \;\; 6x + ky = {c + 1}", str(k), prompt="ถ้าเส้นตรงสองเส้นนี้ขนานกัน ค่าของ k เท่ากับเท่าใด",
                        distractors=_tk4(str(-k), frac_tex(Fraction(a * b, 6)), str(6 * b), str(k + 1), answer=str(k)))


@question_type("math.perpendicular_lines_k_m4", display_name={"th": "ค่า k ที่ทำให้เส้นตรงสองเส้นตั้งฉากกัน"}, level=LEVEL,
               topic="เรขาคณิตวิเคราะห์")
class PerpendicularLinesKM4(MathType):
    def expr(self, rng: Random):
        m = _nz4(rng, 1, 6)
        c1, c2 = rng.randint(-9, 9), rng.randint(-9, 9)
        right = Fraction(-1, m)
        return MathDraw(rf"y = {poly_tex((m, 'x'), (c1, ''))}, \;\; y = kx {'+' if c2 >= 0 else '-'} {abs(c2)}", frac_tex(right),
                        prompt="ถ้าเส้นตรงสองเส้นนี้ตั้งฉากกัน ค่าของ k เท่ากับเท่าใด",
                        distractors=_fk4(Fraction(1, m), -m, m, Fraction(-2, m), answer=right))
