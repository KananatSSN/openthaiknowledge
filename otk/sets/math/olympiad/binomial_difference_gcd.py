"""gcd(((3m)^e − m^e)/(2m)², (2m)²), computed exactly with big integers."""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 9",))


def difference_gcd(m: int, e: int) -> int:
    """(3m)^e − m^e = m^e(3^e − 1); divide by (2m)² and take the gcd with
    (2m)² (source: m = 45, e = 90 → 4050)."""
    square = (2 * m) ** 2
    return gcd(((3 * m) ** e - m**e) // square, square)


@question_type(
    "math.binomial_difference_gcd_olympiad",
    display_name={"th": "ห.ร.ม. ของผลต่างกำลังหารด้วยกำลังสอง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class BinomialDifferenceGcd(WordProblem):
    def expr(self, rng: Random):
        while True:
            m, e = rng.randint(3, 60), 2 * rng.randint(2, 50)
            if ((3 * m) ** e - m**e) % (2 * m) ** 2 == 0:
                break
        answer = difference_gcd(m, e)
        square = (2 * m) ** 2
        wrong = [v for v in dict.fromkeys([square, gcd((3 * m) ** e - m**e, square), m * m, answer // 2 if answer % 2 == 0 else answer * 2, gcd(3**e - 1, square)]) if v != answer]
        return MathDraw(
            rf"\gcd\left(\frac{{{3 * m}^{{{e}}}-{m}^{{{e}}}}}{{{2 * m}^2}},\ {2 * m}^2\right)",
            str(answer),
            prompt="จงหา ห.ร.ม. ต่อไปนี้",
            hint=f"ดึง {m}^{e} ออกมาเป็นตัวประกอบ แล้วนับกำลังของ 2, 3, 5 และจำนวนเฉพาะอื่นใน 3^{e} − 1 ด้วยการยกกำลัง (lifting the exponent)",
            distractors=[str(v) for v in wrong],
        )
