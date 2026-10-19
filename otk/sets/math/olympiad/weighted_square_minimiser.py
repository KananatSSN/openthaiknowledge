"""Minimise αx² + βy² + γz² on x + y + z = s: each variable is proportional to its reciprocal weight."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 7",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def minimiser(weights: tuple[int, int, int], s: int) -> tuple[Fraction, ...]:
    """Cauchy–Schwarz: (Σ wᵢxᵢ²)(Σ 1/wᵢ) ≥ (Σ xᵢ)², with equality when wᵢxᵢ
    is constant, so xᵢ = s(1/wᵢ)/Σ(1/wⱼ) (source: 2, 3, 4 with s = 1 → x = 6/13)."""
    inv = [Fraction(1, w) for w in weights]
    return tuple(s * v / sum(inv) for v in inv)


@question_type(
    "math.weighted_square_minimiser_olympiad",
    display_name={"th": "ค่าของตัวแปรที่ทำให้ผลบวกกำลังสองถ่วงน้ำหนักต่ำสุด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class WeightedSquareMinimiser(WordProblem):
    def expr(self, rng: Random):
        weights = tuple(rng.sample(range(1, 10), 3))
        s = rng.randint(1, 6)
        which = rng.randint(0, 2)
        point = minimiser(weights, s)
        answer = point[which]
        proportional = Fraction(s * weights[which], sum(weights))
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(s, 3), proportional, point[(which + 1) % 3], point[(which + 2) % 3], s / sum(Fraction(1, w) for w in weights)]) if v != answer]
        name = "xyz"[which]
        return MathDraw(
            rf"x+y+z={s},\quad {weights[0]}x^2+{weights[1]}y^2+{weights[2]}z^2",
            frac_tex(answer),
            prompt=f"x, y, z เป็นจำนวนจริง จงหาค่า {name} ที่ทำให้นิพจน์ต่อไปนี้มีค่าต่ำสุด",
            hint="ใช้อสมการโคชี–ชวาร์ซ หรือลากรองจ์ ค่าต่ำสุดเกิดเมื่อ 2x·(สัมประสิทธิ์ของ x) เท่ากันทุกตัวแปร",
            distractors=wrong,
        )
