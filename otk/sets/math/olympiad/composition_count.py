"""Ordered sums of positive integers: 2^(N − 1) − 1 with at least two parts, C(N − 1, k − 1) with exactly k."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 7",))


def composition_tex(total: int, parts: int | None) -> str:
    """Bars in the N − 1 gaps between N ones: any non-empty set of bars gives
    at least two parts (2^(N−1) − 1, source: N = 2548), and k − 1 bars give
    exactly k parts."""
    if parts is None:
        return rf"2^{{{total - 1}}}-1"
    return rf"\binom{{{total - 1}}}{{{parts - 1}}}"


@question_type(
    "math.composition_count_olympiad",
    display_name={"th": "จำนวนวิธีเขียนจำนวนเป็นผลบวกโดยลำดับมีความสำคัญ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การจัดหมู่",
)
class CompositionCount(WordProblem):
    def expr(self, rng: Random):
        total = rng.randint(20, 3000)
        parts = rng.choice([None, rng.randint(3, 9)])
        answer = composition_tex(total, parts)
        if parts is None:
            wrong = [rf"2^{{{total - 1}}}", rf"2^{{{total}}}-1", rf"2^{{{total - 1}}}-2", rf"2^{{{total - 2}}}"]
            what = "สองจำนวนขึ้นไป"
        else:
            wrong = [rf"\binom{{{total + parts - 1}}}{{{parts - 1}}}", rf"\binom{{{total - 1}}}{{{parts}}}", rf"\binom{{{total}}}{{{parts - 1}}}", rf"\binom{{{total - 1}}}{{{parts - 2}}}"]
            what = f"{parts} จำนวนพอดี"
        return MathDraw(
            rf"N={total}",
            answer,
            prompt=f"ต้องการเขียน N ในรูปผลบวกของจำนวนเต็มบวก{what} โดยลำดับมีความสำคัญ จะทำได้ทั้งหมดกี่วิธี",
            hint="เขียน N เป็นเลข 1 เรียงกัน N ตัว แล้วเลือกช่องว่างระหว่างเลข 1 ที่จะใส่เส้นแบ่ง",
            distractors=[t for t in dict.fromkeys(wrong) if t != answer],
        )
