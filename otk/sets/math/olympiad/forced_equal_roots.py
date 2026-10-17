"""Three leading coefficients can force every real root to be equal."""

from __future__ import annotations

from fractions import Fraction
from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันแรก ข้อ 9",)
)


def forced_root(degree: int, lead: int, second: int, third: int) -> Fraction:
    """Σr = −second/lead and Σ_{i<j} rᵢrⱼ = third/lead fix Σr²; when
    n·Σr² = (Σr)², Cauchy–Schwarz forces every root to equal Σr/n."""
    total = Fraction(-second, lead)
    pairs = Fraction(third, lead)
    squares = total * total - 2 * pairs
    if degree * squares != total * total:
        raise ValueError("the roots are not forced equal")
    return total / degree


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


@question_type(
    "math.forced_equal_roots_olympiad",
    display_name={"th": "สัมประสิทธิ์สามตัวแรกบังคับให้รากทุกตัวเท่ากัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="รากของพหุนาม",
)
class ForcedEqualRoots(WordProblem):
    def expr(self, rng: Random):
        degree = rng.randint(3, 7)
        p, q = rng.randint(1, 4), rng.randint(1, 4)
        t = Fraction(-p, q)
        lead = q * q
        second = int(-lead * degree * t)
        third = int(lead * comb(degree, 2) * t * t)
        answer = forced_root(degree, lead, second, third)
        wrong = [frac_tex(v) for v in dict.fromkeys([-answer, answer * 2, answer / 2, Fraction(-second, lead), answer - 1]) if v != answer]
        return MathDraw(
            rf"{lead}x^{{{degree}}}+{second}x^{{{degree - 1}}}+{third}x^{{{degree - 2}}}+\cdots=0",
            frac_tex(answer),
            prompt="สมการพหุนามต่อไปนี้ (สัมประสิทธิ์ที่เหลือเป็นจำนวนจริงใด ๆ) มีรากเป็นจำนวนจริงทั้งหมด จงหารากที่มีค่าน้อยที่สุด",
            hint="หาผลบวกรากและผลบวกกำลังสองของรากจากสูตรของเวียตา แล้วใช้อสมการโคชี–ชวาร์ซ",
            distractors=wrong,
        )
