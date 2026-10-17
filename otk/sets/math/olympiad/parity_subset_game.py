"""Over all nonempty S, a pile with nonempty B goes to the odd side 2^{m−1} times."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2556, ข้อ 11",)
)


def average_share(total: int, m: int) -> Fraction:
    """|B ∩ S| is odd for exactly half of all 2ᵐ subsets S when B ≠ ∅, and
    never for S = ∅; averaging over the 2ᵐ − 1 nonempty S gives more than half."""
    return Fraction(total * 2 ** (m - 1), 2**m - 1)


def _num(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


@question_type(
    "math.parity_subset_game_olympiad",
    display_name={"th": "ค่าเฉลี่ยของเหรียญที่ได้จากเกมภาวะคี่ของสับเซต"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ความน่าจะเป็น",
)
class ParitySubsetGame(WordProblem):
    def expr(self, rng: Random):
        m = rng.randint(2, 6)
        total = rng.randint(10, 200)
        answer = average_share(total, m)
        wrong = [_num(v) for v in dict.fromkeys([
            Fraction(total, 2),  # include S = ∅ in the average
            Fraction(total * (2 ** (m - 1) - 1), 2**m - 1),  # the other player's share
            Fraction(total * 2 ** (m - 1), 2**m),
            Fraction(total * m, 2 * m - 1),
            Fraction(total * (m + 1), 2 * m + 1),
        ]) if v != answer]
        return MathDraw(
            rf"m={m},\quad a_1+\cdots+a_n={total}",
            _num(answer),
            prompt=(
                "มีเหรียญ n กอง กองที่ i มี a_i เหรียญ ผู้เล่นแรกเลือกสับเซตไม่ว่าง B₁, …, B_n ของ {1, …, m} "
                "จากนั้นสุ่มเลือกสับเซตไม่ว่าง S ของ {1, …, m} อย่างสม่ำเสมอ กองที่ i เป็นของผู้เล่นที่สองถ้า |B_i ∩ S| เป็นคี่ "
                "จงหาค่าคาดหมายของจำนวนเหรียญที่ผู้เล่นที่สองได้ (ไม่ขึ้นกับ B_i)"
            ),
            hint="สำหรับ B ไม่ว่าง สับเซต S ครึ่งหนึ่งของทั้งหมด 2ᵐ สับเซตทำให้ |B ∩ S| เป็นคี่ และ S = ∅ ไม่อยู่ในครึ่งนั้น",
            distractors=wrong,
        )
