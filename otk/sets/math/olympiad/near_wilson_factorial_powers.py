"""(p − 2)! ≡ 1 and (p − 3)! ≡ −1/2 (mod p) by Wilson's theorem."""

from __future__ import annotations

from math import factorial
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 10",))


PRIMES = (11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)


def residue(p: int, e1: int, e2: int, f3: int | None = None, f2: int | None = None) -> int:
    """((p − 3)!)^e1 + ((p − 2)!)^e2 mod p. Wilson gives (p − 2)! ≡ 1 and
    (p − 3)! ≡ 1/(p − 2) ≡ −1/2 (source: p = 29, e1 = 26, e2 = 27 → 5).
    f3, f2 override the two factorial residues (for the named mistakes)."""
    if f3 is None:
        f3 = factorial(p - 3) % p
    if f2 is None:
        f2 = factorial(p - 2) % p
    return (pow(f3, e1, p) + pow(f2, e2, p)) % p


@question_type(
    "math.near_wilson_factorial_powers_olympiad",
    display_name={"th": "เศษจากการหารกำลังของแฟกทอเรียลใกล้ทฤษฎีบทวิลสัน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class NearWilsonFactorialPowers(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(PRIMES)
        e1, e2 = rng.randint(2, 3 * p), rng.randint(2, 3 * p)
        answer = residue(p, e1, e2)
        half = pow(2, -1, p)
        wrong = [v for v in dict.fromkeys([residue(p, e1, e2, f3=half), residue(p, e1, e2, f2=p - 1), residue(p, e1, e2, f3=p - 1, f2=1), residue(p, e1, e2, f3=1, f2=1), (answer + 1) % p]) if v != answer]
        return MathDraw(
            rf"({p - 3}!)^{{{e1}}}+({p - 2}!)^{{{e2}}}",
            str(answer),
            prompt=f"จงหาเศษจากการหารจำนวนต่อไปนี้ด้วย {p}",
            hint=f"ทฤษฎีบทวิลสัน: {p - 1}! ≡ −1 (mod {p}) จึงได้ {p - 2}! ≡ 1 และ {p - 3}! ≡ 1/{p - 2} ≡ −1/2 แล้วใช้ทฤษฎีบทแฟร์มาต์ลดเลขชี้กำลัง",
            distractors=[str(v) for v in wrong],
        )
