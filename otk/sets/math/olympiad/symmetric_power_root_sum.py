"""(c − x)ⁿ + xⁿ = 0 is symmetric under x ↦ c − x; for odd n it has degree n − 1."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 16",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def root_sum(c: int, n: int) -> Fraction:
    """For odd n the xⁿ terms cancel, leaving degree n − 1 with leading
    coefficient nc; the next coefficient gives the sum (n − 1)c/2, as the
    roots pair up as x, c − x. For even n the degree is n and the sum nc/2
    (source: c = 2, n = 2005 → 2004)."""
    return Fraction((n - 1) * c, 2) if n % 2 else Fraction(n * c, 2)


@question_type(
    "math.symmetric_power_root_sum_olympiad",
    display_name={"th": "ผลบวกรากของสมการที่สมมาตร"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="รากของพหุนาม",
)
class SymmetricPowerRootSum(WordProblem):
    def expr(self, rng: Random):
        c, n = rng.randint(1, 9), rng.randint(5, 2549)
        answer = root_sum(c, n)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(n * c, 2) if n % 2 else Fraction((n - 1) * c, 2), Fraction(n * c), Fraction((n - 1) * c), Fraction(c, 2), Fraction(n - 1)]) if v != answer]
        return MathDraw(
            rf"({c}-x)^{{{n}}}+x^{{{n}}}=0",
            frac_tex(answer),
            prompt="จงหาผลบวกของรากทั้งหมดของสมการต่อไปนี้ (นับรากเชิงซ้อนด้วย)",
            hint="ถ้า x เป็นราก c − x ก็เป็นราก ตรวจดีกรีของพหุนามก่อน ว่าพจน์ xⁿ หักล้างกันหรือไม่",
            distractors=wrong,
        )
