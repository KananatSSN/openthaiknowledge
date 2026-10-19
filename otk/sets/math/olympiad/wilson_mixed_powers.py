"""Four factorial-power terms modulo 9p, by Wilson modulo p and divisibility modulo 9."""

from __future__ import annotations

from math import factorial
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 15",))


PRIMES = (101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251)


def terms(p: int) -> list[int]:
    """With h = (p − 1)/2: ((p−1)!)^h, h^((p−1)!), (h!)^(p−1), (p−1)^(h!),
    each reduced modulo 9p by Python's modular power."""
    h, modulus = (p - 1) // 2, 9 * p
    big, half = factorial(p - 1), factorial(h)
    return [pow(big, h, modulus), pow(h, big, modulus), pow(half, p - 1, modulus), pow(p - 1, half, modulus)]


def crt(r_p: int, r_9: int, p: int) -> int:
    return next(x for x in range(r_9, 9 * p, 9) if x % p == r_p)


@question_type(
    "math.wilson_mixed_powers_olympiad",
    display_name={"th": "เศษจากการหารผลบวกกำลังของแฟกทอเรียล"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class WilsonMixedPowers(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(PRIMES)
        h, modulus = (p - 1) // 2, 9 * p
        values = terms(p)
        answer = sum(values) % modulus
        wilson_sign = (sum(values[1:]) + crt(1, 0, p)) % modulus
        fermat_slip = (values[0] + crt(h % p, values[1] % 9, p) + values[2] + values[3]) % modulus
        wrong = [v for v in dict.fromkeys([answer % p, wilson_sign, sum(values[1:]) % modulus, fermat_slip, crt(answer % p, 0, p)]) if v != answer]
        return MathDraw(
            rf"({p - 1}!)^{{{h}}}+{h}^{{{p - 1}!}}+({h}!)^{{{p - 1}}}+{p - 1}^{{{h}!}}",
            str(answer),
            prompt=f"จงหาเศษจากการหารจำนวนต่อไปนี้ด้วย {modulus} (= 9 × {p} และ {p} เป็นจำนวนเฉพาะ)",
            hint="หาเศษมอดุโล 9 และมอดุโล p แยกกัน ใช้ทฤษฎีบทวิลสัน (p − 1)! ≡ −1 และทฤษฎีบทแฟร์มาต์ แล้วรวมด้วยทฤษฎีบทเศษเหลือของจีน",
            distractors=[str(v) for v in wrong],
        )
