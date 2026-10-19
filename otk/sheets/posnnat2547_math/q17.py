"""ข้อ 17 — 1²⁵⁴⁷ + 2²⁵⁴⁷ + ⋯ + 2547²⁵⁴⁷ มอดุโล 25

k^E mod M depends only on k mod M: sum one period, times the number of full
periods, plus the tail (for M = 25 and odd E a full period cancels in pairs
k, 25 − k, leaving 2²⁵⁴⁷ + 1 ≡ 4).

``check`` adds all the terms.
"""

from __future__ import annotations

PARAMS = {"last": 2547, "e": 2547, "modulus": 25}
ANSWER = 4
VARIANTS = [{"last": 1000, "e": 100}, {"modulus": 27}, {"last": 358, "e": 2431, "modulus": 49}, {"e": 2548, "modulus": 16}]


def solve(last=2547, e=2547, modulus=25):
    period = sum(pow(k, e, modulus) for k in range(1, modulus + 1))
    tail = sum(pow(k, e, modulus) for k in range(1, last % modulus + 1))
    return (last // modulus * period + tail) % modulus


def check(last=2547, e=2547, modulus=25):
    return sum(pow(k, e, modulus) for k in range(1, last + 1)) % modulus
