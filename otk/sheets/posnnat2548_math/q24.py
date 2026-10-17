"""วันที่สอง ข้อ 3 — มีฟังก์ชัน f : ℕ → ℕ ที่ f(f(n)) = 2n หรือไม่

Yes: f(2ᵏ(4j + 1)) = 2ᵏ(4j + 3) and f(2ᵏ(4j + 3)) = 2ᵏ⁺¹(4j + 1). Any such f
has f(2n) = f(f(f(n))) = 2f(n). The solver uses only that: with f(m) = t,
f(2^j·m) = 2^j·t (side 0) and f(2^j·t) = 2^(j+1)·m (side 1). Here f(1) = 3, so
f(4) = 12.

``check`` evaluates the source's explicit f (so m ≡ 1 mod 4 and t = m + 2 in
every case) and also confirms f(f(n)) = 2n on a range.
"""

from __future__ import annotations

PARAMS = {"m": 1, "t": 3, "j": 2, "side": 0}
ANSWER = 12
VARIANTS = [{"j": 3, "side": 1}, {"m": 5, "t": 7, "j": 1}, {"m": 9, "t": 11, "j": 4, "side": 1}]


def solve(m=1, t=3, j=2, side=0):
    return 2**j * t if side == 0 else 2 ** (j + 1) * m


def check(m=1, t=3, j=2, side=0):
    def f(n):
        k = (n & -n).bit_length() - 1
        odd = n >> k
        return (odd + 2) << k if odd % 4 == 1 else (odd - 2) << (k + 1)

    assert all(f(f(n)) == 2 * n for n in range(1, 2000)) and f(m) == t
    return f(2**j * (m if side == 0 else t))
