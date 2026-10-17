"""a b…b c divisible by the four-digit a b b c: the n repeat with a period."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันแรก ข้อ 3",)
)


def sandwich_mod(a: int, b: int, c: int, n: int, modulus: int) -> int:
    rep = (pow(10, n, 9 * modulus) - 1) // 9 % modulus  # 11…1 with n ones
    return (a * pow(10, n + 1, modulus) + b * 10 * rep + c) % modulus


def next_hit(a: int, b: int, c: int, limit: int = 20000) -> int:
    """The smallest n > 2 with abbc | a b…b c (n copies of b). Writing the
    number with n + k copies as 10^k·(n copies) + (const)(10^k − 1), any k
    with 10^k ≡ 1 modulo the relevant factor repeats the hit."""
    modulus = int(f"{a}{b}{b}{c}")
    for n in range(3, limit):
        if sandwich_mod(a, b, c, n, modulus) == 0:
            return n
    raise ValueError("no second hit below the limit")


def _triples():
    found = []
    for a in range(1, 10):
        for b in range(0, 10):
            for c in (1, 3, 7, 9):
                if b == a and b == c:
                    continue
                try:
                    n = next_hit(a, b, c, 400)
                except ValueError:
                    continue
                found.append((a, b, c, n))
    return tuple(found)


TRIPLES = _triples()


@question_type(
    "math.repdigit_sandwich_divisibility_olympiad",
    display_name={"th": "จำนวนรูป a b…b c ที่หารด้วย abbc ลงตัว"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: เลขโดด",
)
class RepdigitSandwichDivisibility(WordProblem):
    def expr(self, rng: Random):
        a, b, c, answer = rng.choice(TRIPLES)
        modulus = int(f"{a}{b}{b}{c}")
        wrong = [v for v in dict.fromkeys([answer + 1, answer - 1, answer + 2, 2 * answer - 2, answer + 3]) if v != answer and v > 2]
        return MathDraw(
            rf"{a}\underbrace{{{b}{b}\cdots{b}}}_{{n}}{c},\quad {modulus}",
            str(answer),
            prompt=f"เมื่อ n = 2 จำนวนนี้คือ {modulus} เอง จงหาค่า n > 2 ที่น้อยที่สุดที่ทำให้จำนวนนี้หารด้วย {modulus} ลงตัว",
            hint="เขียนจำนวนเป็น a·10^(n+1) + b·(10^n − 1)/9·10 + c แล้วคำนวณเศษทีละ n แบบเวียนเกิด",
            distractors=[str(v) for v in wrong],
        )
