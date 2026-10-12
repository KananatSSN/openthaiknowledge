"""ข้อ 25 — ค่ามากที่สุดที่เป็นไปได้ของ m − n

ให้ m และ n เป็นจำนวนเต็มบวกซึ่ง m ≥ n และ  1/m + 1/n = 2/33
จงหาค่ามากที่สุดที่เป็นไปได้ของ m − n

Clearing denominators, ``k(m + n) = 2mn`` with k = 33, so

    m = k·n / (2n − k)

and m is a positive integer only when ``2n − k`` divides ``kn`` and is positive.
Pushing m as high as possible means pushing the denominator as low as possible:
with k odd, ``2n − k`` is odd too, so its smallest usable value is 1, at
``n = (k+1)/2 = 17``. That gives ``m = 33·17 = 561`` and

    m − n = 561 − 17 = **544**

which in closed form is ``k(k+1)/2 − (k+1)/2 = (k² − 1)/2``. (Checking:
1/17 + 1/561 = 33/561 + 1/561 = 34/561 = 2/33.)

For an even k the denominator ``2n − k`` can be 2 but never 1, so the extreme
pair is ``n = (k+2)/2``, ``m = k(k+2)/4`` — ``solve`` handles both parities from
the divisibility condition rather than from a case split.

``check`` ignores all of that and simply walks n upward over the range where a
solution can exist, keeping the largest difference it actually sees.
"""

from __future__ import annotations

#: 1/m + 1/n = num/k.
PARAMS = {"k": 33, "num": 2}
ANSWER = 544
VARIANTS = [
    {"k": 15, "num": 2},
    {"k": 20, "num": 2},          # even k: the denominator cannot reach 1
    {"k": 7, "num": 2},
    {"k": 12, "num": 1},
    {"k": 30, "num": 3},
    {"k": 9, "num": 4},
    {"k": 5, "num": 7},           # num > 2/n is impossible for any n
]


def _pairs(k: int, num: int):
    """Every (m, n) with m ≥ n ≥ 1 and 1/m + 1/n = num/k."""
    if k <= 0 or num <= 0:
        return []
    out = []
    # n·num > k is forced (else 1/m ≤ 0), and n ≤ 2k/num for m ≥ n.
    for n in range(1, 2 * k // num + 2):
        den = num * n - k
        if den <= 0:
            continue
        if (k * n) % den:
            continue
        m = k * n // den
        if m >= n:
            out.append((m, n))
    return out


def solve(k=33, num=2):
    """The largest m − n over all admissible pairs."""
    pairs = _pairs(k, num)
    if not pairs:
        return None
    return max(m - n for m, n in pairs)


def check(k=33, num=2):
    """Independent: search m instead of n, testing the fraction as written.

    m runs over every value that could possibly work and n is recovered from
    ``1/n = num/k − 1/m`` as an exact rational, kept only when its numerator is
    1 — no divisibility algebra, and the equation is verified in its printed form
    before a pair counts.
    """
    from fractions import Fraction

    if k <= 0 or num <= 0:
        return None
    target = Fraction(num, k)
    best = None
    limit = 2 * k * k + 2 * k
    for m in range(1, limit + 1):
        rest = target - Fraction(1, m)
        if rest <= 0:
            continue
        if rest.numerator != 1:
            continue
        n = rest.denominator
        if n > m:
            continue
        assert Fraction(1, m) + Fraction(1, n) == target
        best = m - n if best is None else max(best, m - n)
    return best
