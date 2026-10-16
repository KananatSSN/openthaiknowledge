"""Lift a simple polynomial root to guarantee many divisors."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def lifted_root(constant: int, exponent: int) -> int:
    """Unique root of a²+a+constant modulo 7**exponent with a=0 mod 7."""
    if constant % 7 or exponent < 1:
        raise ValueError("constant must be divisible by 7 and exponent positive")
    root, modulus = 0, 7
    for _ in range(1, exponent):
        value = root * root + root + constant
        digit = -(value // modulus) * pow(2 * root + 1, -1, 7) % 7
        root += digit * modulus
        modulus *= 7
    return root


@question_type(
    "math.hensel_divisor_lift_olympiad",
    display_name={"th": "ยกรากพหุนามเพื่อสร้างตัวหาร"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class HenselDivisorLift(WordProblem):
    def expr(self, rng: Random):
        constant = 7 * rng.choice((3, 10, 17, 29, 41, 59, 289))
        exponent = rng.randint(2, 5)
        modulus = 7**exponent
        previous_modulus = modulus // 7
        answer = lifted_root(constant, exponent)
        previous = lifted_root(constant, exponent - 1)
        return MathDraw(
            rf"C={constant},\quad k={exponent}",
            str(answer),
            prompt=(
                "จงหาจำนวนเต็ม a ที่ 0≤a<7ᵏ, a หารด้วย 7 ลงตัว "
                "และ a²+a+C หารด้วย 7ᵏ ลงตัว"
            ),
            hint="ยกรากทีละหลัก: แทน a ด้วย a+t·7ʲ แล้วแก้สมการเชิงเส้น modulo 7",
            distractors=[
                str(previous),  # stop one lifting step early
                str((-constant) % modulus),  # discard the quadratic term
                str((-answer) % modulus),  # reverse the root's sign
                str((answer + previous_modulus) % modulus),  # wrong final digit
                str((answer - previous_modulus) % modulus),  # opposite final digit
                str((previous + 7) % modulus),  # shift the initial root only
            ],
        )
