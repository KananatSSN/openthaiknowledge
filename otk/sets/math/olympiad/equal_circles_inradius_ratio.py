"""Equal circles through A, D: AB = AC, then compare the inradii of ABD and ACD."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันแรก ข้อ 2",))

# height h with half-base m and foot offset e: AB² = h² + m², AD² = h² + e²
CONFIGS = ((12, 9, 5), (12, 16, 5), (12, 16, 9), (12, 35, 5), (12, 35, 9), (12, 35, 16), (24, 32, 10), (24, 45, 7), (24, 45, 10))


def frac_tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def inradius_ratio(h: int, m: int, e: int) -> Fraction:
    """Equal circles give ∠ABD = ∠ACD (equal chords AD), so AB = AC. With the
    foot of the altitude at the midpoint of BC, BD = m + e and CD = m − e;
    r = area/semiperimeter, both areas share the height h. The source has
    AB = 15, AD = 13, BC = 18: BD = 14, CD = 4, r₁/r₂ = 4/(3/2) = 8/3."""
    ab = (h * h + m * m) ** 0.5
    ad = (h * h + e * e) ** 0.5
    ab, ad = round(ab), round(ad)
    bd, cd = m + e, m - e
    s1 = Fraction(ab + ad + bd, 2)
    s2 = Fraction(ab + ad + cd, 2)
    return Fraction(bd, 1) / s1 / (Fraction(cd, 1) / s2)


@question_type(
    "math.equal_circles_inradius_ratio_olympiad",
    display_name={"th": "อัตราส่วนรัศมีวงกลมแนบในเมื่อวงกลมสองวงรัศมีเท่ากัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมแนบใน",
)
class EqualCirclesInradiusRatio(WordProblem):
    def expr(self, rng: Random):
        h, m, e = rng.choice(CONFIGS)
        ab, ad = round((h * h + m * m) ** 0.5), round((h * h + e * e) ** 0.5)
        answer = inradius_ratio(h, m, e)
        wrong = [frac_tex(v) for v in dict.fromkeys([1 / answer, Fraction(m + e, m - e), Fraction(m - e, m + e), answer + 1, answer * 2]) if v != answer]
        return MathDraw(
            rf"AB={ab},\quad AD={ad},\quad BC={2 * m},\quad BD>DC",
            frac_tex(answer),
            prompt=(
                "AD เป็นคอร์ดร่วมของวงกลมสองวงที่มีรัศมีเท่ากัน B อยู่บนวงหนึ่ง C อยู่บนอีกวง และ D อยู่บน BC "
                "ให้ r₁, r₂ เป็นรัศมีวงกลมแนบในของ △ABD และ △ACD จงหา r₁/r₂"
            ),
            hint="คอร์ด AD ยาวเท่ากันในวงกลมรัศมีเท่ากัน จึงมุมในส่วนโค้ง ∠ABD = ∠ACD และ AB = AC",
            distractors=wrong,
        )
