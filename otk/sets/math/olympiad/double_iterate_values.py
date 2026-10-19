"""f(f(n)) = 2n gives f(2n) = f(f(f(n))) = 2f(n), so one value fixes a whole chain."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันที่สอง ข้อ 3",))


def chain_value(m: int, t: int, query: tuple[int, int]) -> int:
    """With f(m) = t: f(t) = 2m, and f(2n) = 2f(n). A query (j, side) asks
    f(2^j·m) = 2^j·t (side 0) or f(2^j·t) = 2^(j + 1)·m (side 1). Such f exist:
    pair the odd numbers (o, o′) and set f(2^k o) = 2^k o′, f(2^k o′) = 2^(k+1) o."""
    j, side = query
    return 2**j * t if side == 0 else 2 ** (j + 1) * m


@question_type(
    "math.double_iterate_values_olympiad",
    display_name={"th": "ค่าของฟังก์ชันที่ f(f(n)) = 2n"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class DoubleIterateValues(WordProblem):
    def expr(self, rng: Random):
        while True:
            m, t = 2 * rng.randint(0, 20) + 1, 2 * rng.randint(0, 20) + 1
            if m != t:
                break
        query = (rng.randint(1, 5), rng.randint(0, 1))
        answer = chain_value(m, t, query)
        j, side = query
        point = 2**j * (m if side == 0 else t)
        wrong = [v for v in dict.fromkeys([2 * point, 2**j * m if side == 0 else 2**j * t, chain_value(m, t, (j, 1 - side)), 2 ** (j + 1) * t if side == 0 else 2**j * m, point + t]) if v != answer]
        return MathDraw(
            rf"f(f(n))=2n,\quad f({m})={t}",
            str(answer),
            prompt=f"f : ℕ → ℕ สอดคล้อง f(f(n)) = 2n สำหรับทุกจำนวนนับ n และ f({m}) = {t} จงหา f({point})",
            hint="จาก f(f(f(n))) จะได้ f(2n) = 2f(n) และ f(f(m)) = 2m",
            distractors=[str(v) for v in wrong],
        )
