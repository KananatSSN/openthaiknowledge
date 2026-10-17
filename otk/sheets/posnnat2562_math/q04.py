"""ข้อ 4 — a ที่ N(a) เป็นจำนวนคี่ เมื่อระยะรวม 2019

Modulo 2 the generating function of jump sequences, 1/(1 − Σ tʲ(xʲ + x⁻ʲ)), is
1 + t(x + x⁻¹)/(1 + t²): the coefficient of tᵀ is x + x⁻¹ for odd T and 0 for
even T > 0. So N(a) is odd exactly for a = ±1 when the total is odd. The answer
is the tuple of those a.

``check`` runs the path count modulo 2 directly, one bitset of end points per
total length: N_L = Σⱼ (N_{L−j} shifted by ±j).
"""

from __future__ import annotations

PARAMS = {"total": 2019}
ANSWER = (-1, 1)
VARIANTS = [{"total": 1}, {"total": 8}, {"total": 15}, {"total": 40}]


def solve(total=2019):
    return (-1, 1) if total % 2 else ()


def check(total=2019):
    offset = total
    rows = [1 << offset]
    for length in range(1, total + 1):
        row = 0
        for jump in range(1, length + 1):
            prev = rows[length - jump]
            row ^= (prev << jump) ^ (prev >> jump)
        rows.append(row)
    last = rows[total]
    return tuple(i - offset for i in range(2 * total + 1) if last >> i & 1)
