"""ข้อ 5 — f(m² + n²) = (f(m) − f(n))² + f(2mn), 8f(0) + 9f(1) = 2006, หา f(0)

m = 1, n = 0 gives f(1) − f(0) = (f(1) − f(0))², so f(1) = f(0) + d with
d ∈ {0, 1}; then (α + β)f(0) + βd = N, and only d = 0 is integral here:
f(0) = 118.

``check`` confirms that both families (f ≡ c and f(n) = n + c) satisfy the
equation on a range, then scans c for the one meeting αf(0) + βf(1) = N.
"""

from __future__ import annotations

PARAMS = {"alpha": 8, "beta": 9, "total": 2006}
ANSWER = 118
VARIANTS = [{"alpha": 4, "beta": 11, "total": 791}, {"alpha": 3, "beta": 5, "total": 245}, {"alpha": 7, "beta": 2, "total": 812}]


def solve(alpha=8, beta=9, total=2006):
    found = [(total - beta * d) // (alpha + beta) for d in (0, 1)
             if (total - beta * d) % (alpha + beta) == 0 and total - beta * d >= 0]
    return found[0] if len(found) == 1 else None


def check(alpha=8, beta=9, total=2006):
    for shift in (0, 1):
        def f(x, shift=shift):
            return 7 + shift * x

        assert all(f(m * m + n * n) == (f(m) - f(n)) ** 2 + f(2 * m * n) for m in range(8) for n in range(8))
    hits = [c for c in range(total + 1) for f1 in (c, c + 1) if alpha * c + beta * f1 == total]
    return hits[0] if len(hits) == 1 else None
