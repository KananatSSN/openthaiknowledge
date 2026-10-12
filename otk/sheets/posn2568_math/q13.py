"""ข้อ 13 — ค่ามากที่สุดของ |P(−1)|

ให้ P(x) = a₀ + a₁x + ⋯ + aₙxⁿ มีสัมประสิทธิ์เป็นจำนวนเต็ม โดย
    1) a_k ≥ k สำหรับ k = 0,1,…,n
    2) P(1)  = p1        (โจทย์: 135)
    3) P(10) = p10       (โจทย์: 2025)
ค่ามากที่สุดที่เป็นไปได้ของ |P(−1)| เท่ากับเท่าใด

Method: a_k ≥ k ≥ 0 makes every coefficient non-negative, so P(base) = p10 caps
the degree hard — a degree-n polynomial already needs a_n·baseⁿ ≥ n·baseⁿ. For
the sheet's numbers that forces n = 2, and then P(1) and P(10) are two linear
equations in three unknowns: one free coefficient, a closed interval for it, and
|P(−1)| linear in it — so the maximum sits at an endpoint (a₂ = 19, giving 133).

``solve`` does not assume n = 2: it walks the degrees, pruning on the running
budget. ``check`` is the flat enumeration over every admissible coefficient
tuple, with no pruning at all.
"""

from __future__ import annotations

from itertools import product

PARAMS = {"p1": 135, "p10": 2025, "base": 10}
ANSWER = 133
VARIANTS = [
    {"p1": 20, "p10": 200},
    {"p1": 135, "p10": 1350},
    {"p1": 50, "p10": 500, "base": 10},
    {"p1": 30, "p10": 120, "base": 4},
    {"p1": 8, "p10": 26, "base": 3},
]


def _max_degree(p10: int, base: int) -> int:
    n = 0
    while (n + 1) * base ** (n + 1) <= p10:
        n += 1
    return n


def polynomials(p1=135, p10=2025, base=10):
    """Every admissible coefficient list, low order first."""
    top = _max_degree(p10, base)
    found = []

    def walk(k: int, coeffs: list[int], value: int, total: int):
        if k < 0:
            if value == p10 and total == p1:
                found.append(list(reversed(coeffs)))
            return
        weight = base ** k
        for a in range(k, (p10 - value) // weight + 1):
            if total + a > p1:                 # coefficients are non-negative
                break
            walk(k - 1, coeffs + [a], value + a * weight, total + a)

    for degree in range(top + 1):
        walk(degree, [], 0, 0)
    return found


def solve(p1=135, p10=2025, base=10):
    """Largest |P(−1)| over the admissible polynomials, or None if none exist."""
    values = [abs(sum(a * (-1) ** k for k, a in enumerate(coeffs)))
              for coeffs in polynomials(p1, p10, base)]
    return max(values) if values else None


def check(p1=135, p10=2025, base=10):
    """Independent: enumerate coefficient tuples exhaustively, no pruning."""
    best = None
    for degree in range(_max_degree(p10, base) + 1):
        ranges = [range(k, p10 // base ** k + 1) for k in range(degree + 1)]
        for coeffs in product(*ranges):
            if sum(coeffs) != p1:
                continue
            if sum(a * base ** k for k, a in enumerate(coeffs)) != p10:
                continue
            value = abs(sum(a * (-1) ** k for k, a in enumerate(coeffs)))
            best = value if best is None else max(best, value)
    return best
