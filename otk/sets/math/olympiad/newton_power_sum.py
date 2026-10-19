"""Integer S₁, S₂, S₃ with 6 | 5S₁ − 3S₂ − 2S₃ give integer e₂, e₃, hence every Sₙ."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันแรก ข้อ 7",))


def power_sums(e1: int, e2: int, e3: int, count: int) -> list[int]:
    """Newton: S₁ = e₁, S₂ = e₁S₁ − 2e₂, S₃ = e₁S₂ − e₂S₁ + 3e₃,
    Sₙ = e₁Sₙ₋₁ − e₂Sₙ₋₂ + e₃Sₙ₋₃. The source's condition is exactly that
    e₂ = (S₁² − S₂)/2 and e₃ = (S₁³ − 3S₁S₂ + 2S₃)/6 are integers."""
    s = [3, e1, e1 * e1 - 2 * e2]
    s.append(e1 * s[2] - e2 * s[1] + 3 * e3)
    while len(s) <= count:
        s.append(e1 * s[-1] - e2 * s[-2] + e3 * s[-3])
    return s[1:count + 1]


def elementary(s1: int, s2: int, s3: int) -> tuple[Fraction, Fraction, Fraction]:
    e2 = Fraction(s1 * s1 - s2, 2)
    e3 = Fraction(s1**3 - 3 * s1 * s2 + 2 * s3, 6)
    return Fraction(s1), e2, e3


@question_type(
    "math.newton_power_sum_olympiad",
    display_name={"th": "ผลบวกกำลังจากเอกลักษณ์ของนิวตัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามสมมาตร",
)
class NewtonPowerSum(WordProblem):
    def expr(self, rng: Random):
        e1, e2, e3 = rng.randint(-4, 4), rng.randint(-4, 4), rng.randint(-4, 4)
        s1, s2, s3, s4 = power_sums(e1, e2, e3, 4)
        answer = s4
        wrong = [v for v in dict.fromkeys([s4 + e2 * e2, e1 * s3 - e2 * s2, e1 * s3 + e2 * s2 - e3 * s1, s2 * s2, s4 + 2 * e2 + 1]) if v != answer]
        return MathDraw(
            rf"S_1={s1},\ S_2={s2},\ S_3={s3}",
            str(answer),
            prompt="a, b, c เป็นจำนวนจริง และ Sₙ = aⁿ + bⁿ + cⁿ จงหา S₄",
            hint="หา ab + bc + ca และ abc จาก S₁, S₂, S₃ แล้วใช้ S₄ = e₁S₃ − e₂S₂ + e₃S₁",
            distractors=[str(v) for v in wrong],
        )
