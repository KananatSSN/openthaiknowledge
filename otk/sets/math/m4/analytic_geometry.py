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
