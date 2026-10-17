"""ข้อ 5 — n ห้าหลักที่ 2556 | n³ − 1 และผลรวมเลขโดดน้อยที่สุด

The solver lists the residues r mod M with r³ ≡ 1 and walks each through the
d-digit range in steps of M, keeping the numbers of least digit sum. The
answer is the tuple of all such n (2556, five digits: 21301 alone).

``check`` tests every d-digit number directly.
"""

from __future__ import annotations

PARAMS = {"modulus": 2556, "digits": 5}
ANSWER = (21301,)
VARIANTS = [{"modulus": 284, "digits": 5}, {"modulus": 852, "digits": 4},
            {"modulus": 1092, "digits": 5}, {"modulus": 1988, "digits": 4}]


def _digit_sum(n):
    return sum(map(int, str(n)))


def solve(modulus=2556, digits=5):
    low, high = 10 ** (digits - 1), 10**digits
    found = []
    for r in range(modulus):
        if pow(r, 3, modulus) != 1 % modulus:
            continue
        found.extend(range(low + (r - low) % modulus, high, modulus))
    best = min(map(_digit_sum, found))
    return tuple(sorted(n for n in found if _digit_sum(n) == best))


def check(modulus=2556, digits=5):
    hits = [n for n in range(10 ** (digits - 1), 10**digits) if (n**3 - 1) % modulus == 0]
    best = min(_digit_sum(n) for n in hits)
    return tuple(n for n in hits if _digit_sum(n) == best)
