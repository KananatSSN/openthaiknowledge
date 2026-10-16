"""Use Wilson's theorem to reduce a near-complete residue product."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def consecutive_product_residue(prime: int, first_residue: int) -> int:
    """Product of p-3 consecutive residues starting at 1, 2, or 3."""
    if prime < 7 or first_residue not in (1, 2, 3):
        raise ValueError("expected prime >= 7 and first residue 1, 2, or 3")
    missing = prime - 1 if first_residue == 2 else 2
    return -pow(missing, -1, prime) % prime


@question_type(
    "math.wilson_consecutive_product_olympiad",
    display_name={"th": "ผลคูณจำนวนเรียงกันด้วยทฤษฎีบทวิลสัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class WilsonConsecutiveProduct(WordProblem):
    def expr(self, rng: Random):
        prime = rng.choice((7, 23, 31, 47, 71, 79, 103))
        first_residue = rng.randint(1, 3)
        first = prime * rng.randint(1, 4) + first_residue
        answer = consecutive_product_residue(prime, first_residue)
        inverse_two = pow(2, -1, prime)
        return MathDraw(
            rf"p={prime},\quad a={first}",
            str(answer),
            prompt="จงหาเศษเหลือของผลคูณจำนวนเต็มตั้งแต่ a ถึง a+p−4 เมื่อหารด้วย p",
            hint="ผลคูณครอบคลุมจำนวนที่ไม่เป็นศูนย์ modulo p ทุกตัว ยกเว้นสองตัว",
            distractors=[
                "0",  # assume the run contains a multiple of p
                "1",  # assume the omitted factors multiply to Wilson's residue
                str(prime - 1),  # forget the two excluded factors in Wilson's theorem
                str(inverse_two),  # lose Wilson's negative sign
                str(2),  # multiply by missing factors instead of dividing
                str(prime - 2),  # retain Wilson's sign but not the inverse
            ],
        )
