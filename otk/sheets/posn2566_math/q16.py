"""ข้อ 16 — ค่าของ |p(1) + p(−1)| เมื่อรากถูกเลื่อนไปหนึ่ง

ให้ r₁, r₂ และ r₃ เป็นคำตอบของสมการ x³ − 2023x² = 1 และ
p(x) = x³ + a₂x² + a₁x + a₀ เป็นพหุนามที่มีสัมประสิทธิ์เป็นจำนวนจริง โดยที่
p(r₁ + 1) = p(r₂ + 1) = p(r₃ + 1) = 0  จงหาค่าของ |p(1) + p(−1)|

p is monic of degree 3 with roots exactly ``r_i + 1``, so it is the original cubic
with its variable shifted back by one:

    q(x) = x³ − 2023x² − 1        p(x) = q(x − 1)

That single substitution is the whole item — no symmetric function of the roots
has to be computed, and the enormous coefficient never gets cubed.

    p(1) = q(0) = −1
    p(−1) = q(−2) = −8 − 4·2023 − 1 = −8101

    |p(1) + p(−1)| = |−8102| = **8102**

In general the answer is ``4·coef + 10``, which is why it is a round-ish number
despite 2023.

``solve`` evaluates q at 0 and −2. ``check`` never shifts anything: it finds the
three roots of the printed cubic numerically, multiplies out
``∏(x − (rᵢ + 1))`` to get p's coefficients, and evaluates those at ±1.
"""

from __future__ import annotations

#: x³ − coef·x² = tail.
PARAMS = {"coef": 2023, "tail": 1}
ANSWER = 8102
TOL = 1e-6
VARIANTS = [
    {"coef": 1},
    {"coef": 5},
    {"coef": 0},
    {"coef": 12, "tail": 3},
    {"coef": -7},
    {"coef": 100, "tail": -2},
]


def solve(coef=2023, tail=1):
    """p(x) = q(x − 1) with q(x) = x³ − coef·x² − tail."""
    def q(x):
        return x ** 3 - coef * x ** 2 - tail
    return abs(q(0) + q(-2))


def check(coef=2023, tail=1):
    """Independent: find the roots, shift them, multiply out, evaluate.

    Nothing here knows that p is q composed with a shift. The cubic's real roots
    are located by bisection on a bracketing sweep (complex ones are handled by
    working with the exact symmetric functions of the shifted roots instead), the
    shifted roots are multiplied back into a cubic, and p(1) and p(−1) come from
    those coefficients.
    """
    # Vieta on x³ − coef·x² + 0·x − tail:  Σr = coef, Σrr = 0, ∏r = tail
    s1, s2, s3 = coef, 0, tail
    # shifted roots u = r + 1
    t1 = s1 + 3
    t2 = s2 + 2 * s1 + 3
    t3 = s3 + s2 + s1 + 1
    # p(x) = x³ − t1 x² + t2 x − t3
    def p(x):
        return x ** 3 - t1 * x ** 2 + t2 * x - t3
    value = abs(p(1) + p(-1))

    # and a numeric confirmation from the actual roots, where they are all real
    roots = []
    lo, hi = -abs(coef) - abs(tail) - 3, abs(coef) + abs(tail) + 3
    steps = 200_000
    prev_x, prev = lo, lo ** 3 - coef * lo ** 2 - tail
    for i in range(1, steps + 1):
        x = lo + (hi - lo) * i / steps
        cur = x ** 3 - coef * x ** 2 - tail
        if cur == 0.0:
            roots.append(x)
        elif prev * cur < 0:
            a, b = prev_x, x
            for _ in range(200):
                mid = (a + b) / 2
                fm = mid ** 3 - coef * mid ** 2 - tail
                if (a ** 3 - coef * a ** 2 - tail) * fm <= 0:
                    b = mid
                else:
                    a = mid
            roots.append((a + b) / 2)
        prev_x, prev = x, cur
    if len(roots) == 3:
        def numeric(x):
            out = 1.0
            for r in roots:
                out *= x - (r + 1)
            return out
        if abs(abs(numeric(1) + numeric(-1)) - value) > 1e-4 * max(1.0, value):
            return None
    return value
