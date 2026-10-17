"""Recover m + n from m² + n² and gcd + lcm."""

from __future__ import annotations

from math import gcd, isqrt
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2551, วันแรก ข้อ 7",))


def pairs_for(square_sum: int, gl_sum: int) -> list[tuple[int, int]]:
    """With g = gcd, m = gu, n = gv: g²(u² + v²) = S and g(1 + uv) = T. A
    direct scan over m ≤ √S finds every pair. The source (3789, 633) has
    g = 3, u, v = 14, 15: m + n = 87."""
    found = []
    for m in range(1, isqrt(square_sum) + 1):
        rest = square_sum - m * m
        n = isqrt(rest)
        if n >= m and n * n == rest:
            g = gcd(m, n)
            if g + m * n // g == gl_sum:
                found.append((m, n))
    return found


def _cases():
    out = []
    for m in range(2, 80):
        for n in range(m + 1, 80):
            s, t = m * m + n * n, gcd(m, n) + m * n // gcd(m, n)
            if gcd(m, n) > 1 and pairs_for(s, t) == [(m, n)]:
                out.append((s, t, m + n))
    return tuple(out[::5])


CASES = _cases()


@question_type(
    "math.gcd_lcm_square_sum_olympiad",
    display_name={"th": "หา m + n จากผลบวกกำลังสองและ ห.ร.ม. + ค.ร.น."},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวน: ห.ร.ม. และ ค.ร.น.",
)
class GcdLcmSquareSum(WordProblem):
    def expr(self, rng: Random):
        s, t, answer = rng.choice(CASES)
        wrong = [v for v in dict.fromkeys([answer + 2, answer - 2, isqrt(2 * s), answer + 6, isqrt(s) + 1]) if v != answer and v > 0]
        return MathDraw(
            rf"m^2+n^2={s},\quad (m,n)+[m,n]={t}",
            str(answer),
            prompt="m, n เป็นจำนวนเต็มบวก (m, n) และ [m, n] คือ ห.ร.ม. และ ค.ร.น. จงหา m + n",
            hint="ให้ g = (m, n), m = gu, n = gv แล้ว g² หาร m² + n² และ g หาร (m, n) + [m, n]",
            distractors=[str(v) for v in wrong],
        )
