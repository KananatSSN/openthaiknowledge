"""Coprime m, n with p | (ab)^m + a^n − 2b^n, found through a table of powers of ab."""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันที่สอง ข้อ 5",))


PRIMES = (101, 103, 107, 109, 113, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 409, 1009, 2549)
BASES = ((25, 49), (9, 16), (4, 25), (16, 81))


def solutions(p: int, a: int, b: int, coprime: bool = True) -> list[tuple[int, int, int]]:
    """For each n < p find the least m ≥ 1 with (ab)^m ≡ 2bⁿ − aⁿ (mod p)
    (and gcd(m, n) = 1 if asked), from a table of the powers of ab
    (source: p = 2549, a = 25, b = 49: m = 1, n = 45)."""
    table: dict[int, list[int]] = {}
    x = 1
    for m in range(1, p):
        x = x * a * b % p
        table.setdefault(x, []).append(m)
    out = []
    for n in range(1, p):
        target = (2 * pow(b, n, p) - pow(a, n, p)) % p
        for m in table.get(target, []):
            if not coprime or gcd(m, n) == 1:
                out.append((m + n, n, m))
                break
    return sorted(out)


@question_type(
    "math.coprime_exponent_pair_olympiad",
    display_name={"th": "คู่เลขชี้กำลังที่เป็นจำนวนเฉพาะสัมพัทธ์ซึ่งทำให้หารลงตัว"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class CoprimeExponentPair(WordProblem):
    def expr(self, rng: Random):
        while True:
            p = rng.choice(PRIMES)
            a, b = rng.choice(BASES)
            found = solutions(p, a, b)
            if len(found) >= 2:
                break
        answer = found[0][0]
        loose = solutions(p, a, b, coprime=False)[0][0]
        wrong = [v for v in dict.fromkeys([loose, found[0][1], found[1][0], min(n for _, n, _ in found), found[0][2] + 2 * found[0][1]]) if v != answer]
        return MathDraw(
            rf"{p}\mid ({a}\cdot {b})^m+{a}^n-2\cdot {b}^n,\quad (m,n)=1",
            str(answer),
            prompt=f"m, n เป็นจำนวนนับที่เป็นจำนวนเฉพาะสัมพัทธ์กัน ({p} เป็นจำนวนเฉพาะ) จงหาค่าน้อยที่สุดของ m + n ที่สอดคล้องเงื่อนไข",
            hint=f"คิดมอดุโล {p}: ทำตารางค่า ({a}·{b})^m แล้วสำหรับแต่ละ n หา m ที่ทำให้ ({a}·{b})^m ≡ 2·{b}ⁿ − {a}ⁿ โดยตรวจ (m, n) = 1",
            distractors=[str(v) for v in wrong],
        )
