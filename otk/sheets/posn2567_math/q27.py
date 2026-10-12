"""ข้อ 27 — จำนวนสมาชิกของเซต A

ให้ p และ q เป็นจำนวนเฉพาะที่แตกต่างกัน  ให้ A เป็นเซตของจำนวนเต็มบวก n ทั้งหมด
ที่ทำให้สมการ p²⁰x² + nx + q²⁴ = 0 มีคำตอบทุกคำตอบเป็นจำนวนตรรกยะ
จงหาจำนวนสมาชิกของเซต A

Rational roots mean the quadratic factors over the integers, and by unique
factorisation the only factorisations are

    p^e x² + nx + q^f = (p^i x + q^{f-j})(p^{e-i} x + q^{j}),

so n = p^i q^j + p^{e-i} q^{f-j} for 0 ≤ i ≤ e, 0 ≤ j ≤ f. That is (e+1)(f+1)
pairs, but swapping the two factors — (i, j) ↦ (e-i, f-j) — gives the same n, so

    |A| = ((e+1)(f+1) + F) / 2,   F = 1 if e and f are both even, else 0

(F counts the one self-paired factorisation, i = e/2 and j = f/2). For e = 20 and
f = 24 that is (525 + 1)/2 = **263**.

Note what does *not* matter: the primes themselves. ``PARAMS`` still carries them
so the variants can move them and ``check`` — which builds the actual set of n and
counts it — would catch a ``solve`` that had smuggled in a dependence.
"""

from __future__ import annotations

from math import isqrt

#: the two distinct primes and their exponents.
PARAMS = {"p": 2, "q": 3, "ep": 20, "eq": 24}
ANSWER = 263
VARIANTS = [
    {"p": 5, "q": 7},                          # same exponents, other primes
    {"p": 2, "q": 3, "ep": 4, "eq": 6},
    {"p": 3, "q": 11, "ep": 3, "eq": 4},       # one odd exponent: no fixed point
    {"p": 2, "q": 5, "ep": 1, "eq": 1},
    {"p": 2, "q": 5, "ep": 0, "eq": 0},        # both constant: one n only
    {"p": 2, "q": 2, "ep": 4, "eq": 4},        # not distinct primes
]


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    return all(n % f for f in range(2, isqrt(n) + 1))


def solve(p=2, q=3, ep=20, eq=24):
    """|A| = ((e+1)(f+1) + F)/2 — factorisations, paired by swapping the factors."""
    if not (_is_prime(p) and _is_prime(q)) or p == q or ep < 0 or eq < 0:
        return None
    pairs = (ep + 1) * (eq + 1)
    fixed = 1 if ep % 2 == 0 and eq % 2 == 0 else 0
    return (pairs + fixed) // 2


def check(p=2, q=3, ep=20, eq=24):
    """Independent: build every n that factors, count the distinct ones.

    For small exponents it also scans n directly and keeps those whose
    discriminant is a perfect square — the definition of "all roots rational" —
    and asserts the two agree, which is what ties the factorisation argument to
    the question as asked.
    """
    if not (_is_prime(p) and _is_prime(q)) or p == q or ep < 0 or eq < 0:
        return None
    values = {p ** i * q ** j + p ** (ep - i) * q ** (eq - j)
              for i in range(ep + 1) for j in range(eq + 1)}

    four_ac = 4 * p ** ep * q ** eq
    if four_ac <= 10 ** 6:                     # small enough to scan n outright
        top = max(values)
        scanned = set()
        for n in range(1, top + 1):
            disc = n * n - four_ac
            if disc < 0:
                continue
            root = isqrt(disc)
            if root * root == disc:
                scanned.add(n)
        assert scanned == values, sorted(scanned ^ values)[:6]
    return len(values)
