"""Non-increasing maps {1..m} → {1..n} are multisets of size m: C(m + n − 1, m)."""

from __future__ import annotations

from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 12",))


def map_count(m: int, n: int) -> int:
    """A non-increasing f is fixed by the multiset of its values: m values from
    n kinds with repetition (source: m = n gives C(2n − 1, n))."""
    return comb(m + n - 1, m)


@question_type(
    "math.nonincreasing_function_count_olympiad",
    display_name={"th": "จำนวนฟังก์ชันไม่เพิ่ม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การจัดหมู่",
)
class NonincreasingFunctionCount(WordProblem):
    def expr(self, rng: Random):
        m, n = rng.randint(2, 12), rng.randint(2, 12)
        answer = map_count(m, n)
        wrong = [v for v in dict.fromkeys([comb(m + n, m), n**m, comb(n, m) if comb(n, m) else comb(m + n - 2, m), comb(m + n - 1, m - 1), comb(m + n - 1, m) * 2]) if v != answer]
        return MathDraw(
            rf"f:\{{1,\ldots,{m}\}}\to\{{1,\ldots,{n}\}},\quad x<y\Rightarrow f(x)\ge f(y)",
            str(answer),
            prompt="จงหาจำนวนฟังก์ชันทั้งหมดที่มีสมบัติต่อไปนี้",
            hint="ฟังก์ชันไม่เพิ่มถูกกำหนดด้วยค่าที่ใช้และจำนวนครั้งที่ใช้ เป็นการเลือกแบบซ้ำได้",
            distractors=[str(v) for v in wrong],
        )
