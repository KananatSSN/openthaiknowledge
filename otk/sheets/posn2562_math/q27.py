"""ข้อ 27 — ค่าของ k

สำหรับจำนวนเต็มบวก n ≥ 2 ใด ๆ นิยาม f(n) เป็นตัวประกอบที่ใหญ่ที่สุดของ n ที่ไม่ใช่
ตัวมันเอง กำหนดให้ a₁ = 2019²⁵⁶² และสำหรับจำนวนเต็มบวก n ใด ๆ ซึ่ง aₙ ≥ 2 เป็น
จำนวนเต็มบวก นิยาม aₙ₊₁ = aₙ − f(aₙ)  ถ้า a_k คือพจน์แรกของลำดับนี้ที่มีค่าน้อยกว่า 2
แล้ว k มีค่าเท่าใด (หมายเหตุ 673 เป็นจำนวนเฉพาะ)

The largest proper divisor of n is ``n/p`` with p the **smallest** prime factor,
so the step is

    aₙ₊₁ = aₙ − aₙ/p = aₙ·(p − 1)/p

— one copy of p leaves the factorisation and the factorisation of ``p − 1``
arrives in its place. Because the process always attacks the smallest prime, the
debris from one removal is cleared before the next copy of a larger prime is
touched, so the step count is **additive**: writing T(p) for the total number of
removals caused by one copy of p,

    T(p) = 1 + Σ_q e_q(p − 1)·T(q),      S(n) = Σ_p e_p(n)·T(p)

With 2019 = 3 · 673 (the note is there for exactly this),

    T(2) = 1,  T(3) = 1 + T(2) = 2,  T(7) = 1 + T(2) + T(3) = 4
    672 = 2⁵·3·7  ⟹  T(673) = 1 + 5·T(2) + T(3) + T(7) = 12

    S(2019²⁵⁶²) = 2562·T(3) + 2562·T(673) = 2562 · 14 = 35868

and a₁ is the first term, so the first term below 2 is

    k = 35868 + 1 = **35869**

``solve`` evaluates that recursion — no sequence is ever walked. ``check`` walks
it: it keeps the current term as a multiset of primes and applies the printed
step one at a time, counting until nothing is left.
"""

from __future__ import annotations

from functools import lru_cache

#: a₁ = base^exponent.
PARAMS = {"base": 2019, "exponent": 2562}
ANSWER = 35869
VARIANTS = [
    {"base": 2019, "exponent": 1},
    {"base": 2, "exponent": 10},
    {"base": 12, "exponent": 5},
    {"base": 673, "exponent": 3},
    {"base": 97, "exponent": 4},
    {"base": 1, "exponent": 5},          # a₁ = 1 is already below 2
]


def _factorise(n: int) -> dict[int, int]:
    """Prime factorisation by trial division — every prime here stays small."""
    out: dict[int, int] = {}
    factor = 2
    while factor * factor <= n:
        while n % factor == 0:
            out[factor] = out.get(factor, 0) + 1
            n //= factor
        factor += 1 if factor == 2 else 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


@lru_cache(maxsize=None)
def removals(prime: int) -> int:
    """T(p): removals caused by one copy of p, including its own."""
    if prime <= 2:
        return 1
    return 1 + sum(e * removals(q) for q, e in _factorise(prime - 1).items())


def solve(base=2019, exponent=2562):
    """k = 1 + Σ over the prime factors of a₁ of multiplicity × T(p)."""
    if base < 1 or exponent < 0:
        return None
    if base == 1 or exponent == 0:
        return 1                          # a₁ = 1 is already below 2
    steps = sum(e * exponent * removals(p)
                for p, e in _factorise(base).items())
    return steps + 1


def check(base=2019, exponent=2562):
    """Independent: walk the sequence, one printed step at a time.

    The current term is held as a multiset of primes. Each step finds the
    smallest prime present — that is what makes n/p the largest proper divisor —
    removes one copy of it and folds in the factorisation of p − 1, exactly as
    ``aₙ₊₁ = aₙ(p − 1)/p`` says. The terms are counted until nothing is left.
    """
    if base < 1 or exponent < 0:
        return None
    if base == 1 or exponent == 0:
        return 1
    live = {p: e * exponent for p, e in _factorise(base).items()}
    index = 1
    guard = 0
    while any(live.values()):
        guard += 1
        if guard > 10 ** 6:
            return None
        smallest = min(p for p, e in live.items() if e > 0)
        live[smallest] -= 1
        if live[smallest] == 0:
            del live[smallest]
        for q, e in _factorise(smallest - 1).items():
            live[q] = live.get(q, 0) + e
        index += 1
    return index
