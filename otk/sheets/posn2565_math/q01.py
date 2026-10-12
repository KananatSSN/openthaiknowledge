"""ข้อ 1 — ค่าของ ab/(bc + ca)

ถ้า a, b และ c เป็นจำนวนจริงบวกซึ่งสอดคล้องกับสมการ 2^a = 3^b = 216^c
แล้วค่าของ ab/(bc + ca) เท่ากับเท่าใด

Divide numerator and denominator by abc:

    ab/(bc + ca) = (1/c) / (1/a + 1/b).

With 2^a = 3^b = N^c = k, taking logs gives 1/a = ln2/ln k, 1/b = ln3/ln k and
1/c = ln N/ln k, so the ln k cancels and

    ab/(bc + ca) = ln N / (ln 2 + ln 3) = ln N / ln 6.

For N = 216 = 6³ that is **3**. The value is rational only when N is a power of
the product of the two bases — for N = 2^p 3^q with p ≠ q it is an irrational
combination of logarithms, which the sheet's phrasing ("เท่ากับเท่าใด") cannot
ask for, so ``solve`` returns ``None`` there and the generator never draws it.
"""

from __future__ import annotations

import math
from fractions import Fraction

#: 2^a = 3^b = (base1^p · base2^q)^c
PARAMS = {"base1": 2, "base2": 3, "p": 3, "q": 3}
ANSWER = 3
VARIANTS = [
    {"p": 5, "q": 5},
    {"base1": 2, "base2": 5, "p": 4, "q": 4},
    {"base1": 3, "base2": 7, "p": 1, "q": 1},
    {"p": 2, "q": 5},                     # irrational: no exact answer to state
    {"base1": 2, "base2": 2, "p": 3, "q": 3},   # not two distinct bases
]
TOL = 1e-12


def solve(base1=2, base2=3, p=3, q=3):
    """ln N / ln(base1·base2) — an integer exactly when the exponents match."""
    if min(base1, base2) < 2 or base1 == base2 or p < 1 or q < 1:
        return None
    if p != q:
        return None
    return Fraction(p)


def check(base1=2, base2=3, p=3, q=3):
    """Independent: pick a value for the common power and measure the ratio.

    a, b and c are read off from an arbitrary k by logarithms and the expression
    is evaluated as written — no algebra from ``solve`` is reused, and the answer
    coming out the same for two very different k is itself the claim that the
    ratio does not depend on k.
    """
    if min(base1, base2) < 2 or base1 == base2 or p < 1 or q < 1:
        return None
    if p != q:
        return None
    n = base1 ** p * base2 ** q
    values = []
    for k in (7.0, 1234.5):                  # two unrelated common values
        lk = math.log(k)
        a, b, c = lk / math.log(base1), lk / math.log(base2), lk / math.log(n)
        values.append(a * b / (b * c + c * a))
    assert abs(values[0] - values[1]) < 1e-9, values
    return Fraction(values[0]).limit_denominator(10 ** 6)
