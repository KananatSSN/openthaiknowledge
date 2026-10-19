"""Smallest digit sum of a d-digit n with n³ ≡ 1 modulo M."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2556, ข้อ 5",)
)

MODULI = (2556, 284, 852, 1278, 1988, 2412, 1092, 2044, 3285)


def cube_roots_of_one(modulus: int) -> list[int]:
    return [r for r in range(modulus) if pow(r, 3, modulus) == 1 % modulus]


def smallest_digit_sum(modulus: int, digits: int) -> int:
    """Walk the residues r with r³ ≡ 1 through the d-digit range."""
    low, high = 10 ** (digits - 1), 10**digits
    best = None
    for r in cube_roots_of_one(modulus):
        start = low + (r - low) % modulus
        for n in range(start, high, modulus):
            s = sum(map(int, str(n)))
            if best is None or s < best:
                best = s
    if best is None:
        raise ValueError("no such number")
    return best


@question_type(
    "math.cube_root_unity_digit_sum_olympiad",
    display_name={"th": "ผลบวกเลขโดดน้อยสุดของ n ที่ n³ − 1 หารด้วย M ลงตัว"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เลขคณิตมอดุลาร์",
)
class CubeRootUnityDigitSum(WordProblem):
    def expr(self, rng: Random):
        modulus = rng.choice(MODULI)
        digits = rng.choice([4, 5])
        answer = smallest_digit_sum(modulus, digits)
        wrong = [v for v in dict.fromkeys([1, answer + 3, answer - 3, answer + 1, answer + 6, answer - 1]) if v > 0 and v != answer]
        return MathDraw(
            rf"{modulus}\ \Big|\ n^3-1",
            str(answer),
            prompt=f"n เป็นจำนวนเต็มบวก {digits} หลัก ซึ่ง n³ − 1 หารด้วย {modulus} ลงตัว ผลบวกเลขโดดของ n มีค่าน้อยสุดเท่าใด",
            hint="แยก M เป็นกำลังของจำนวนเฉพาะ หาเศษของ n ในแต่ละมอดุลัส (ถ้า q ≡ 2 mod 3 จะได้ n ≡ 1) แล้วใช้ผลบวกเลขโดดมอดุโล 3 หรือ 9",
            distractors=[str(v) for v in wrong],
        )
