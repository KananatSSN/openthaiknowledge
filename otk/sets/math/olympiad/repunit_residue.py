"""The k-digit repunit modulo M is (10^k − 1)/9 mod M, computed through 10^k mod 9M."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 13",))


def repunit_mod(k: int, modulus: int) -> int:
    """R_k = (10^k − 1)/9; taking 10^k mod 9M keeps the division exact
    (source: k = 1862, M = 2006 → 781)."""
    return (pow(10, k, 9 * modulus) - 1) // 9 % modulus


@question_type(
    "math.repunit_residue_olympiad",
    display_name={"th": "เศษจากการหารจำนวนที่มีเลขโดดเป็น 1 ทั้งหมด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การหารลงตัวและเศษเหลือ",
)
class RepunitResidue(WordProblem):
    def expr(self, rng: Random):
        k, modulus = rng.randint(100, 3000), rng.randint(500, 3000)
        answer = repunit_mod(k, modulus)
        wrong = [v for v in dict.fromkeys([(pow(10, k, modulus) - 1) % modulus, repunit_mod(k - 1, modulus), repunit_mod(k + 1, modulus), k % modulus, repunit_mod(k % modulus, modulus)]) if v != answer]
        return MathDraw(
            rf"\underbrace{{11\ldots1}}_{{{k}}}",
            str(answer),
            prompt=f"จงหาเศษจากการหารจำนวนที่ประกอบด้วยเลข 1 ติดกัน {k} ตัว ด้วย {modulus}",
            hint=f"เขียนเป็น (10^{k} − 1)/9 แยก {modulus} เป็นตัวประกอบ หรือหาคาบของ 10 มอดุโลตัวประกอบแต่ละตัว",
            distractors=[str(v) for v in wrong],
        )
