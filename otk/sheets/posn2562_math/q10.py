"""ข้อ 10 — ค่าของ mn

กำหนดให้ f(x) = x³ + mx² + nx + p โดยที่ p เป็นจำนวนเฉพาะบวก และ m, n เป็นจำนวนเต็ม
ถ้า f(x) หารด้วย x − 1 แล้วเหลือเศษ 4 แต่หารด้วย x + 3 ลงตัว จงหาค่าของ mn

The two remainder conditions are two linear equations in three unknowns:

    f(1)  = 1 + m + n + p = 4      ⟹  m + n = 3 − p
    f(−3) = −27 + 9m − 3n + p = 0  ⟹  9m − 3n = 27 − p

Eliminating n gives ``12m = 36 − 4p``, i.e. **m = 3 − p/3** — so the family only
lands on integers when ``3 | p``, and the one positive prime divisible by 3 is
``p = 3``. Then m = 2, n = −2 and

    mn = **−4**.

The primality is doing real work: without it every p ≡ 0 (mod 3) would give
another (m, n) pair and there would be no single answer.

``solve`` walks the primes and solves the 2×2 system exactly for each; ``check``
sweeps m and n over a range and tests both printed divisions by actually dividing
the polynomial, never touching the elimination.
"""

from __future__ import annotations

from fractions import Fraction

#: f(u) = ru and f(v) = rv, with p a positive prime.
PARAMS = {"u": 1, "ru": 4, "v": -3, "rv": 0}
ANSWER = -4
VARIANTS = [
    {"u": 1, "ru": 0, "v": -3, "rv": 0},
    {"u": 1, "ru": 8, "v": -3, "rv": 0},
    {"u": 1, "ru": 0, "v": 2, "rv": 4},
    {"u": 1, "ru": 1, "v": 2, "rv": 0},
    {"u": 1, "ru": 4, "v": 1, "rv": 4},        # the same point twice
    {"u": 1, "ru": 6, "v": -3, "rv": 0},       # no prime makes m an integer
]
PRIMES = [n for n in range(2, 200)
          if all(n % f for f in range(2, int(n ** 0.5) + 1))]


def coefficients(u=1, ru=4, v=-3, rv=0):
    """(m, n, p) forced by the two remainders and p prime — or None."""
    hits = []
    for p in PRIMES:
        # u³ + m·u² + n·u + p = ru   and   v³ + m·v² + n·v + p = rv
        a1, b1, c1 = u * u, u, Fraction(ru - u ** 3 - p)
        a2, b2, c2 = v * v, v, Fraction(rv - v ** 3 - p)
        det = a1 * b2 - a2 * b1
        if det == 0:
            continue
        m = (c1 * b2 - c2 * b1) / det
        n = (a1 * c2 - a2 * c1) / det
        if m.denominator == 1 and n.denominator == 1:
            hits.append((int(m), int(n), p))
    return hits


def solve(u=1, ru=4, v=-3, rv=0):
    """mn, when the primality of p pins the family down to one member."""
    hits = coefficients(u, ru, v, rv)
    if len(hits) != 1:
        return None
    m, n, _ = hits[0]
    return m * n


def check(u=1, ru=4, v=-3, rv=0, span=60):
    """Independent: sweep the coefficients and divide the polynomial for real.

    Every (m, n, p) in range is tried, the cubic is divided by each printed
    linear factor with synthetic division, and the pair is kept only when both
    remainders come out as printed and p is prime — no elimination, no formula.
    """
    hits = set()
    prime = set(PRIMES)

    def remainder(coefs, root):
        """Synthetic division of the cubic by (x − root)."""
        acc = 0
        for coef in coefs:
            acc = acc * root + coef
        return acc

    for p in sorted(prime):
        if p > span:
            break
        for m in range(-span, span + 1):
            for n in range(-span, span + 1):
                cubic = (1, m, n, p)
                if remainder(cubic, u) == ru and remainder(cubic, v) == rv:
                    hits.add((m, n, p))
    if len(hits) != 1:
        return None
    m, n, _ = next(iter(hits))
    return m * n
