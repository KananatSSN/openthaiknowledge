"""ข้อ 7 — 5 | ma² + b² ⇒ m ≡ n² (mod 5)  (พิสูจน์)

p ∤ a (else p | b too), so m ≡ −(b/a)², and −1 is a square mod p for
p ≡ 1 (mod 4): m ≡ (i·b/a)². The solver returns the smaller square root of m in
1..p − 1 (p = 5, a = 1, b = 2: m ≡ 1, root 1).

``check`` finds m from the divisibility by search and then the root by search.
"""

from __future__ import annotations

PARAMS = {"p": 5, "a": 1, "b": 2}
ANSWER = 1
VARIANTS = [{"p": 13, "a": 3, "b": 5}, {"p": 17, "a": 2, "b": 9}, {"p": 29, "a": 7, "b": 4}]


def solve(p=5, a=1, b=2):
    i = next(t for t in range(2, p) if t * t % p == p - 1)
    root = i * b * pow(a, -1, p) % p
    return min(root, p - root)


def check(p=5, a=1, b=2):
    m = next(m for m in range(p) if (m * a * a + b * b) % p == 0)
    return min(n for n in range(1, p) if (n * n - m) % p == 0)
