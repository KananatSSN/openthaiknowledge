"""วันที่สอง ข้อ 6 — ไม่มีจำนวนเฉพาะ p, q, r (p > r, q > r) ที่ pq | rᵖ + r^q  (พิสูจน์)

When p, q > r, Fermat gives rᵖ + r^q ≡ r + r^q (mod p), so r^(q−1) ≡ −1 (mod p),
and the orders of r force a contradiction. The solver counts the triples of
primes ≤ L with p, q > r and pq | rᵖ + r^q by modular powers: 0.

``check`` computes rᵖ + r^q exactly as integers and divides.
"""

from __future__ import annotations

PARAMS = {"limit": 60}
ANSWER = 0
VARIANTS = [{"limit": 10}, {"limit": 30}, {"limit": 80}]


def _primes(limit):
    return [p for p in range(2, limit + 1) if all(p % d for d in range(2, int(p**0.5) + 1))]


def solve(limit=60):
    primes = _primes(limit)
    return sum(1 for r in primes for p in primes for q in primes
               if p > r and q > r and (pow(r, p, p * q) + pow(r, q, p * q)) % (p * q) == 0)


def check(limit=60):
    primes = _primes(limit)
    return sum(1 for r in primes for p in primes for q in primes
               if p > r and q > r and (r**p + r**q) % (p * q) == 0)
