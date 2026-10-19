"""p | ma² + b² with p ≡ 1 (mod 4) makes m a square mod p: n ≡ i·b/a."""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2555, ข้อ 7",)
)

PRIMES = (5, 13, 17, 29, 37, 41)


def square_root_of_m(p: int, a: int, b: int) -> int:
    """p ∤ a (else p | b too), so m ≡ −(b/a)²; −1 ≡ i² because p ≡ 1 mod 4,
    hence m ≡ (i·b/a)². Returns the smaller of the two roots in 1..p − 1."""
    i = next(t for t in range(2, p) if t * t % p == p - 1)
    root = i * b * pow(a, -1, p) % p
    return min(root, p - root)


@question_type(
    "math.fifth_power_residue_square_olympiad",
    display_name={"th": "m เป็นกำลังสองมอดุโล p เมื่อ p หาร ma² + b²"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class FifthPowerResidueSquare(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(PRIMES)
        while True:
            a, b = rng.randint(1, 4 * p), rng.randint(1, 4 * p)
            if gcd(a, b) == 1 and a % p and b % p:
                break
        m = (-b * b * pow(a * a, -1, p)) % p
        answer = square_root_of_m(p, a, b)
        plain = b * pow(a, -1, p) % p
        wrong = [v for v in dict.fromkeys([min(plain, p - plain), m, (p - 1) // 2, min(b % p, p - b % p), (answer + 1) % p or 1]) if v != answer and v > 0]
        return MathDraw(
            rf"p={p},\ a={a},\ b={b},\quad {p}\mid ma^2+b^2,\ 0\le m<{p}",
            str(answer),
            prompt=f"จงหาจำนวนเต็มบวก n ที่น้อยที่สุดซึ่ง {p} หาร m − n² ลงตัว",
            hint="a ไม่เป็นพหุคูณของ p จึงหารได้: m ≡ −(b/a)² (mod p) และ −1 เป็นกำลังสองมอดุโล p เมื่อ p ≡ 1 (mod 4)",
            distractors=[str(v) for v in wrong],
        )
