"""วันที่สอง ข้อ 5 — มี (m, n) = 1 ที่ 2549 | (25·49)ᵐ + 25ⁿ − 2·49ⁿ  (พิสูจน์ด้วยตัวอย่าง)

For each n < p the solver looks up the least m with (ab)^m ≡ 2bⁿ − aⁿ (mod p)
in a table of powers of ab, keeping only gcd(m, n) = 1, and returns the least
m + n: 46, from m = 1, n = 45, which is the witness the proof needs.

``check`` searches the pairs by increasing m + n directly.
"""

from __future__ import annotations

from math import gcd

PARAMS = {"p": 2549, "a": 25, "b": 49}
ANSWER = 46
VARIANTS = [{"p": 113}, {"p": 211, "a": 9, "b": 16}, {"p": 101, "a": 4, "b": 25}, {"p": 409}]


def solve(p=2549, a=25, b=49):
    table = {}
    x = 1
    for m in range(1, p):
        x = x * a * b % p
        table.setdefault(x, []).append(m)
    best = None
    for n in range(1, p):
        target = (2 * pow(b, n, p) - pow(a, n, p)) % p
        for m in table.get(target, []):
            if gcd(m, n) == 1:
                best = m + n if best is None else min(best, m + n)
                break
    return best


def check(p=2549, a=25, b=49):
    for total in range(2, 2 * p):
        for m in range(1, total):
            n = total - m
            if gcd(m, n) == 1 and (pow(a * b, m, p) + pow(a, n, p) - 2 * pow(b, n, p)) % p == 0:
                return total
    return None
