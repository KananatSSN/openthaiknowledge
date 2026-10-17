"""gcd of aₙ = 2^(3n − i) + 3^(6n − j) + 5^(6n − k): each term is constant modulo small primes."""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 12",))


def term(n: int, shifts: tuple[int, int, int]) -> int:
    i, j, k = shifts
    return 2 ** (3 * n - i) + 3 ** (6 * n - j) + 5 ** (6 * n - k)


def sequence_gcd(shifts: tuple[int, int, int], last: int) -> int:
    """gcd(a₁, …, a_N), exactly: gcd(g, aₙ) = gcd(g, aₙ mod g), and aₙ mod g
    comes from modular powers (source: shifts 1, 2, 3 → 14)."""
    i, j, k = shifts
    g = term(1, shifts)
    for n in range(2, last + 1):
        g = gcd(g, (pow(2, 3 * n - i, g) + pow(3, 6 * n - j, g) + pow(5, 6 * n - k, g)) % g)
        if g == 1:
            break
    return g


CASES = tuple(s for s in ((i, j, k) for i in range(3) for j in range(6) for k in range(6)) if sequence_gcd(s, 4) % 3 == 0 or sequence_gcd(s, 4) > 4)


@question_type(
    "math.exponential_sequence_gcd_olympiad",
    display_name={"th": "ห.ร.ม. ของลำดับผลบวกเลขยกกำลัง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class ExponentialSequenceGcd(WordProblem):
    def expr(self, rng: Random):
        shifts = rng.choice(CASES)
        last = rng.randint(5, 2549)
        answer = sequence_gcd(shifts, last)
        first = term(1, shifts)
        wrong = [v for v in dict.fromkeys([first, gcd(first, term(2, shifts)) * 2, answer // 2 if answer % 2 == 0 else answer * 2, max(f for f in (2, 3, 5, 7, 11, 13) if answer % f == 0) if answer > 1 else 2, 1]) if v != answer]
        i, j, k = shifts

        def exp(c: int, s: int) -> str:
            return f"{c}n" + (f"-{s}" if s else "")

        return MathDraw(
            rf"a_n=2^{{{exp(3, i)}}}+3^{{{exp(6, j)}}}+5^{{{exp(6, k)}}},\quad \gcd(a_1,a_2,\ldots,a_{{{last}}})",
            str(answer),
            prompt="จงหาค่า ห.ร.ม. ต่อไปนี้",
            hint="คำนวณ a₁ ก่อน ตัวหารร่วมต้องหาร a₁ แล้วตรวจแต่ละตัวประกอบเฉพาะ p ของ a₁ ว่า aₙ ≡ 0 (mod p) ทุก n หรือไม่ (เช่น 2³ ≡ 1 และ 3⁶ ≡ 5⁶ ≡ 1 มอดุโล 7)",
            distractors=[str(v) for v in wrong],
        )
