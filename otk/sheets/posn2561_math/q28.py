"""ข้อ 28 — ความน่าจะเป็นที่กบอยู่ที่จุดหนึ่งหลังการกระโดดหลายครั้ง

มีกบตัวหนึ่งอยู่ที่จุด x = 0 บนเส้นจำนวน โดยในการกระโดดแต่ละครั้ง มันจะกระโดดได้ไกล
หนึ่งหน่วยไปทางซ้ายหรือทางขวาด้วยความน่าจะเป็นเท่า ๆ กัน จงหาความน่าจะเป็นที่หลังจาก
การกระโดดครั้งที่ 2561 กบตัวนี้จะมาอยู่ที่จุด x = 2018 บนเส้นจำนวนนี้

Every jump changes x by ±1, so after n jumps ``x ≡ n (mod 2)``: the frog's
position and its jump count always have the same parity. **2561 is odd and 2018
is even**, so the answer is **0** and none of the binomial machinery is needed.

The general count, for what it is worth: with u jumps to the right the frog lands
at ``2u − n``, so the probability is ``C(n, (n+x)/2) / 2ⁿ`` when (n + x) is even
and |x| ≤ n, and zero otherwise. The item exists to see whether you check the
parity before reaching for that.

``solve`` tests the parity and then uses the binomial. ``check`` does not know
about parity at all: it sums ``C(n, u)`` over *every* u from 0 to n whose landing
point ``2u − n`` is the one asked about, building the binomials by the
multiplicative recurrence. When no u qualifies the sum is empty and the answer
falls out as zero on its own.
"""

from __future__ import annotations

from fractions import Fraction
from math import comb

#: n jumps of ±1 from the origin; the probability of finishing at `position`.
PARAMS = {"steps": 2561, "position": 2018}
ANSWER = 0
VARIANTS = [
    {"steps": 4, "position": 2},
    {"steps": 7, "position": 2},          # parity mismatch, in miniature
    {"steps": 10, "position": 0},
    {"steps": 5, "position": 5},
    {"steps": 6, "position": 8},          # out of reach entirely
    {"steps": 2560, "position": 2018},
    {"steps": 12, "position": -4},
]


def _snap(value: Fraction):
    return int(value) if value.denominator == 1 else value


def solve(steps=2561, position=2018):
    """C(n, (n+x)/2)/2ⁿ, once the parity allows it at all."""
    if steps < 0:
        return None
    if abs(position) > steps or (steps + position) % 2:
        return 0
    right = (steps + position) // 2
    return _snap(Fraction(comb(steps, right), 1 << steps))


def check(steps=2561, position=2018):
    """Independent: scan every possible number of right-jumps.

    ``u`` right-jumps and ``n − u`` left-jumps land the frog at ``2u − n``. Every
    u from 0 to n is tried and the ones that finish at the right place have their
    ``C(n, u)`` added in — the binomials come from the recurrence
    ``C(n, u+1) = C(n, u)·(n − u)/(u + 1)``, so no factorial and no parity test
    appears anywhere.
    """
    if steps < 0:
        return None
    ways = 0
    binomial = 1
    for right in range(steps + 1):
        if 2 * right - steps == position:
            ways += binomial
        binomial = binomial * (steps - right) // (right + 1)
    return _snap(Fraction(ways, 1 << steps))
