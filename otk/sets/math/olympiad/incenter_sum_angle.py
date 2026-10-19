"""CA + AI = BC forces B = A/2: mark D on CB with CD = CA, then AI = DB."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันที่สอง ข้อ 1",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def angle_b(angle_a: int) -> Fraction:
    """Take D on BC with CD = CA. CI bisects ∠C, so triangles CAI and CDI are
    congruent: DI = AI = DB and ∠CDI = ∠CAI = A/2. Then ∠IBD = ∠BID and the
    exterior angle at D gives A/2 = 2·(B/2), so B = A/2 (source: A = 70° →
    35°)."""
    return Fraction(angle_a, 2)


@question_type(
    "math.incenter_sum_angle_olympiad",
    display_name={"th": "มุมของรูปสามเหลี่ยมจากเงื่อนไข CA + AI = BC"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมแนบใน",
)
class IncenterSumAngle(WordProblem):
    def expr(self, rng: Random):
        angle_a = 2 * rng.randint(15, 59)
        answer = angle_b(angle_a)
        ask_c = rng.random() < 0.4
        value = 180 - angle_a - answer if ask_c else answer
        wrong_values = [Fraction(angle_a), Fraction(angle_a, 3), Fraction(90 - angle_a // 2), Fraction(180 - angle_a, 2), 180 - angle_a - Fraction(angle_a, 3)]
        if ask_c:
            wrong_values = [180 - angle_a - v for v in wrong_values[:3]] + [Fraction(angle_a, 2), Fraction(180 - angle_a, 2)]
        wrong = [frac_tex(v) + r"^\circ" for v in dict.fromkeys(wrong_values) if v != value and v > 0]
        return MathDraw(
            rf"\angle A={angle_a}^\circ,\quad CA+AI=BC",
            frac_tex(value) + r"^\circ",
            prompt=f"รูปสามเหลี่ยม ABC มีเส้นแบ่งครึ่งมุมภายในตัดกันที่ I และสอดคล้องเงื่อนไขต่อไปนี้ จงหามุม {'C' if ask_c else 'B'}",
            hint="หาจุด D บน BC ที่ CD = CA แล้วสามเหลี่ยม CAI และ CDI เท่ากันทุกประการ จึง DI = AI = DB",
            distractors=wrong,
        )
