"""5 | n²·2^(2n²) + 1 depends only on n mod 10."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 12",))


def divisible_count(last: int, parity: int | None) -> int:
    """Even n: 4^(n²) ≡ 1, so n² ≡ −1, n ≡ 2, 3 (mod 5). Odd n: 4^(n²) ≡ 4,
    so n² ≡ 1, n ≡ 1, 4 (mod 5). Counted by direct modular evaluation
    (source: even n ≤ 100 → 20)."""
    return sum(1 for n in range(last + 1) if (parity is None or n % 2 == parity) and (n * n * pow(2, 2 * n * n, 5) + 1) % 5 == 0)


@question_type(
    "math.power_tower_divisible_count_olympiad",
    display_name={"th": "จำนวน n ที่ทำให้ 5 หาร n²·2^(2n²) + 1"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การหารลงตัวและเศษเหลือ",
)
class PowerTowerDivisibleCount(WordProblem):
    def expr(self, rng: Random):
        last = rng.randint(30, 400)
        parity = rng.choice([0, 1, None])
        answer = divisible_count(last, parity)
        other = divisible_count(last, 1 - parity) if parity is not None else divisible_count(last, 0)
        wrong = [v for v in dict.fromkeys([other, (last + 1) // 5, sum(1 for n in range(last + 1) if (parity is None or n % 2 == parity) and n % 5 in (2, 3)), answer + 1, 2 * answer]) if v != answer]
        kind = {0: "จำนวนเต็มคู่", 1: "จำนวนเต็มคี่", None: "จำนวนเต็ม"}[parity]
        return MathDraw(
            rf"0\le n\le {last},\quad 5\mid n^2\cdot 2^{{2n^2}}+1",
            str(answer),
            prompt=f"มี{kind} n กี่จำนวนที่สอดคล้องเงื่อนไขต่อไปนี้",
            hint="2^(2n²) = 4^(n²) และ 4^k ≡ 1 หรือ 4 (mod 5) ตามที่ k คู่หรือคี่ แล้วแก้ n² ≡ … (mod 5)",
            distractors=[str(v) for v in wrong],
        )
