"""x ↦ x^e is a bijection on odd residues mod 2^K for odd e, so x^e ≡ −1 forces x ≡ −1."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 11",))


def least_root_tex(k: int, e: int) -> str:
    """For odd e, x^e ≡ y^e (mod 2^K) with x, y odd forces x ≡ y, since
    (x^e − y^e)/(x − y) is a sum of e odd terms. (−1)^e = −1, so the least
    positive x is 2^K − 1 (source: K = 2548, e = 2005)."""
    return rf"2^{{{k}}}-1"


@question_type(
    "math.odd_power_root_mod_two_power_olympiad",
    display_name={"th": "จำนวนเต็มบวกน้อยสุดที่ทำให้ 2^K หาร x^e + 1"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class OddPowerRootModTwoPower(WordProblem):
    def expr(self, rng: Random):
        k, e = rng.randint(20, 3000), 2 * rng.randint(1, 1500) + 1
        answer = least_root_tex(k, e)
        wrong = [t for t in dict.fromkeys([rf"2^{{{k}}}+1", rf"2^{{{k - 1}}}-1", rf"2^{{{k}}}-{e}", rf"2^{{{k - 1}}}+1"]) if t != answer]
        return MathDraw(
            rf"2^{{{k}}}\mid x^{{{e}}}+1",
            answer,
            prompt="จงหาจำนวนเต็มบวก x ที่น้อยที่สุดที่สอดคล้องเงื่อนไขต่อไปนี้",
            hint="เลขชี้กำลังเป็นจำนวนคี่ ฟังก์ชัน x ↦ x^e จึงเป็นหนึ่งต่อหนึ่งบนจำนวนคี่มอดุโล 2^K และ (−1)^e = −1",
            distractors=wrong,
        )
