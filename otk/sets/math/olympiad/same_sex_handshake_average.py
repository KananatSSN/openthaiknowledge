"""Expected same-sex neighbours in a random row of m boys and n girls."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันที่สอง ข้อ 5",))


def frac_tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def handshake_average(m: int, n: int) -> Fraction:
    """Each of the m + n − 1 neighbouring pairs is same-sex with probability
    (C(m, 2) + C(n, 2))/C(m + n, 2); linearity gives (m(m − 1) + n(n − 1))/(m + n)."""
    return Fraction(m * (m - 1) + n * (n - 1), m + n)


@question_type(
    "math.same_sex_handshake_average_olympiad",
    display_name={"th": "ค่าเฉลี่ยจำนวนการจับมือของคนเพศเดียวกันที่ยืนติดกัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ความน่าจะเป็น",
)
class SameSexHandshakeAverage(WordProblem):
    def expr(self, rng: Random):
        m, n = rng.randint(2, 15), rng.randint(2, 15)
        answer = handshake_average(m, n)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(m + n - 2), Fraction(m + n - 1, 2), Fraction(m * m + n * n, m + n), Fraction(2 * m * n, m + n), answer + 1]) if v != answer]
        return MathDraw(
            rf"m={m},\quad n={n}",
            frac_tex(answer),
            prompt="นักเรียนชาย m คนและหญิง n คนยืนเรียงแถวแบบสุ่ม คนเพศเดียวกันที่ยืนติดกันจับมือกัน จงหาค่าเฉลี่ยของจำนวนการจับมือ",
            hint="ใช้ความเป็นเชิงเส้นของค่าคาดหมาย: แต่ละคู่ที่ยืนติดกันเป็นเพศเดียวกันด้วยความน่าจะเป็นเท่ากัน",
            distractors=wrong,
        )
