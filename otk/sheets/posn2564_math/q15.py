"""ข้อ 15 — จำนวนสามสิ่งอันดับ (a,b,c) ที่ (a+3)^(b^c) หารด้วย 4 ลงตัว

จงหาจำนวนของสามสิ่งอันดับ (a,b,c) ทั้งหมดที่ a,b,c ∈ {1,2,3,4,5} และ
(a+3)^(b^c) หารด้วย 4 ลงตัว

Only the base's 2-adic valuation matters. With a + 3 running over 4, 5, 6, 7, 8:

* **a = 1** → 4^m, valuation 2m ≥ 2 always — all 25 triples;
* **a = 5** → 8^m, valuation 3m ≥ 2 always — all 25;
* **a = 3** → 6^m, valuation m, so 4 | 6^m exactly when **m ≥ 2**, and the
  exponent b^c equals 1 only when b = 1 — so 4·5 = 20 triples;
* **a = 2, 4** → odd base, never.

Total **70**. The whole question is the single boundary case a = 3, b = 1.

``solve`` counts by that valuation argument, never forming b^c. ``check``
evaluates the printed expression instead — modularly, via ``pow(base, b**c,
divisor)`` — for every triple.
"""

from __future__ import annotations

#: (a + shift)^(b^c) divisible by `divisor`, with a,b,c in 1…top.
PARAMS = {"shift": 3, "top": 5, "divisor": 4}
ANSWER = 70
VARIANTS = [
    {"shift": 3, "top": 5, "divisor": 8},
    {"shift": 3, "top": 4, "divisor": 4},
    {"shift": 1, "top": 5, "divisor": 4},
    {"shift": 3, "top": 5, "divisor": 9},
    {"shift": 0, "top": 6, "divisor": 4},
    {"shift": 2, "top": 5, "divisor": 27},
]


def _valuation(n, p):
    """The exponent of p in n."""
    count = 0
    while n % p == 0:
        n //= p
        count += 1
    return count


def _factor(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def solve(shift=3, top=5, divisor=4):
    """Count by prime valuations: base^m is divisible iff every v_p(base)·m ≥ e_p.

    For each base the requirement collapses to a single threshold on the exponent
    m = b^c, and the number of (b, c) with b^c ≥ threshold is counted directly.
    """
    if top < 1 or divisor < 2 or shift < 0:
        return None
    need = _factor(divisor)
    total = 0
    for a in range(1, top + 1):
        base = a + shift
        if base <= 1:
            continue
        thresholds = []
        for p, e in need.items():
            v = _valuation(base, p)
            if v == 0:
                thresholds = None
                break
            thresholds.append(-(-e // v))          # ceil(e / v)
        if thresholds is None:
            continue
        need_m = max(thresholds) if thresholds else 1
        total += sum(1 for b in range(1, top + 1) for c in range(1, top + 1)
                     if b ** c >= need_m)
    return total


def check(shift=3, top=5, divisor=4):
    """Independent: evaluate (a+shift)^(b^c) mod divisor for every triple."""
    if top < 1 or divisor < 2 or shift < 0:
        return None
    if top > 8:
        return None
    return sum(1
               for a in range(1, top + 1)
               for b in range(1, top + 1)
               for c in range(1, top + 1)
               if pow(a + shift, b ** c, divisor) == 0)
