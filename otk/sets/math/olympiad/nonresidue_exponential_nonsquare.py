"""A·Bⁿ − C·Dⁿ is never a square when it is a quadratic non-residue modulo p for every n."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันแรก ข้อ 8",))

PRIMES = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)


def witness_prime(a: int, b: int, c: int, d: int) -> int:
    """The smallest prime p for which A·Bⁿ − C·Dⁿ (n ≥ 1) is always a
    non-residue mod p (checked over one period, n = 1, …, p − 1). For the
    source 2551·543ⁿ − 2008·7ⁿ, p = 3 works (the value is ≡ 2), and so does
    p = 7 (it is 3·4ⁿ, a non-residue)."""
    for p in PRIMES:
        squares = {x * x % p for x in range(p)}
        if all((a * pow(b, n, p) - c * pow(d, n, p)) % p not in squares for n in range(1, p)):
            return p
    raise ValueError("no witness prime")


def _cases():
    out = []
    for p in (5, 7, 11, 13):
        non = [r for r in range(1, p) if r not in {x * x % p for x in range(p)}]
        for a_res in non[:2]:
            for b_res in (1, 4 % p):
                a = a_res + p * 37
                b = b_res + p * 11
                c, d = 100 + p, p * 3
                try:
                    if witness_prime(a, b, c, d) == p:
                        out.append((a, b, c, d, p))
                except ValueError:
                    pass
    return tuple(out)


CASES = _cases()


@question_type(
    "math.nonresidue_exponential_nonsquare_olympiad",
    display_name={"th": "มอดุลัสที่พิสูจน์ว่านิพจน์ไม่เป็นกำลังสองสมบูรณ์"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class NonresidueExponentialNonsquare(WordProblem):
    def expr(self, rng: Random):
        a, b, c, d, answer = rng.choice(CASES)
        wrong = [v for v in (3, 5, 7, 11, 13, 17) if v != answer][:5]
        return MathDraw(
            rf"{a}\cdot{b}^n-{c}\cdot{d}^n",
            str(answer),
            prompt="จำนวนเฉพาะ p ที่น้อยที่สุดซึ่งนิพจน์ต่อไปนี้ไม่เป็นกำลังสองมอดุโล p ทุกจำนวนเต็มบวก n (จึงไม่เป็นกำลังสองสมบูรณ์) คือข้อใด",
            hint="หาเศษของแต่ละพจน์มอดุโล p สังเกตตัวที่หารด้วย p ลงตัว แล้วเทียบกับเศษกำลังสองมอดุโล p",
            distractors=[str(v) for v in wrong],
        )
