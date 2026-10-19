"""k + (k + d) + … + (k + d(m − 1)) = N means m(2k + d(m − 1)) = 2N."""

from __future__ import annotations

from math import isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 13",))


def odd_starts(total: int, step: int) -> list[int]:
    """Each divisor m of 2N gives 2k = 2N/m − d(m − 1); keep odd positive k
    (source: N = 1372, d = 5 → k = 181 with m = 7)."""
    found = []
    for m in divisors(2 * total):
        twice = 2 * total // m - step * (m - 1)
        if twice > 0 and twice % 2 == 0 and twice // 2 % 2 == 1:
            found.append(twice // 2)
    return sorted(found)


def divisors(n: int) -> list[int]:
    small = [d for d in range(1, isqrt(n) + 1) if n % d == 0]
    return sorted(set(small + [n // d for d in small]))


def _cases():
    out = []
    for step in (3, 4, 5, 6, 7):
        for total in range(200, 3000, 7):
            ks = odd_starts(total, step)
            if 1 <= len(ks) <= 3 and ks != [total]:
                out.append((total, step))
    return tuple(out)


CASES = _cases()


@question_type(
    "math.odd_step_sum_terms_olympiad",
    display_name={"th": "พจน์แรกที่เป็นจำนวนคี่ของอนุกรมเลขคณิตที่มีผลบวกกำหนด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อนุกรมเลขคณิต",
)
class OddStepSumTerms(WordProblem):
    def expr(self, rng: Random):
        total, step = rng.choice(CASES)
        ks = odd_starts(total, step)
        answer = sum(ks)
        all_k = []
        for m in divisors(2 * total):
            twice = 2 * total // m - step * (m - 1)
            if twice > 0 and twice % 2 == 0:
                all_k.append(twice // 2)
        wrong = [v for v in dict.fromkeys([sum(all_k), max(ks), min(ks), sum(ks) + total, sum(all_k) - sum(ks)]) if v != answer and v > 0]
        return MathDraw(
            rf"k+(k+{step})+(k+{2 * step})+\cdots+(k+{step}(m-1))={total}",
            str(answer),
            prompt="จงหาผลบวกของจำนวนเต็มบวกคี่ k ทั้งหมดที่ทำให้มีจำนวนเต็มบวก m ซึ่งสอดคล้องสมการต่อไปนี้",
            hint="ผลบวกอนุกรมเลขคณิตเป็น m(2k + d(m − 1))/2 จึง m หาร 2N ไล่ตัวหาร m แล้วตรวจว่า k เป็นจำนวนเต็มบวกคี่",
            distractors=[str(v) for v in wrong],
        )
