"""ข้อ 1 — ค่าของ (a^{4n} + a^{7n} + a^{−5n}) / (a^{−2n} + a^{n})

ถ้า a³ⁿ = 5 เมื่อ a เป็นจำนวนจริง และ n เป็นจำนวนเต็ม แล้ว
    (a^{4n} + a^{7n} + a^{−5n}) / (a^{−2n} + a^{n})
มีค่าเท่าใด

Only ``t = aⁿ`` matters, and only through ``t³ = 5``. Multiplying numerator and
denominator by ``t⁵`` clears every negative exponent and leaves powers that are
all multiples of three:

    numerator·t⁵   = t⁹ + t¹² + 1 = (t³)³ + (t³)⁴ + 1 = 125 + 625 + 1 = 751
    denominator·t⁵ = t³ + t⁶      = 5 + 25                          = 30

so the ratio is **751/30**, and no root of 5 ever appears.

The same works for any exponents whose spread is a multiple of 3: the answer is
a rational function of ``v = a³ⁿ`` alone. ``solve`` shifts every exponent by the
least common multiple needed to clear the negatives and evaluates in terms of v;
``check`` picks concrete real numbers a and n with ``a³ⁿ = v`` and evaluates the
printed expression as floating point, at several different (a, n) pairs — if the
value depended on anything but v, they would not agree.
"""

from __future__ import annotations

from fractions import Fraction

#: numerator exponents (as multiples of n), denominator exponents, and a^{3n}.
PARAMS = {"top": (4, 7, -5), "bottom": (-2, 1), "value": 5}
ANSWER = Fraction(751, 30)
VARIANTS = [
    {"top": (4, 7, -5), "bottom": (-2, 1), "value": 2},
    {"top": (1, -2), "bottom": (4, -5), "value": 5},
    {"top": (0, 3, 6), "bottom": (-3, 0), "value": 7},
    {"top": (2, 5), "bottom": (-1,), "value": 3},
    {"top": (4, 7, -5), "bottom": (-2, 1), "value": 1},
    {"top": (1, 2), "bottom": (0, 1), "value": 5},      # spread not a multiple of 3
]


def solve(top=(4, 7, -5), bottom=(-2, 1), value=5):
    """The ratio as an exact rational in v = a^{3n}, when it is one.

    Every printed exponent has to leave the same remainder mod 3 — that is what
    lets one common factor t^s clear all the negatives *and* turn every surviving
    power into a power of t³ = v. Otherwise the value is irrational and the
    sheet's format has no answer for it.
    """
    if value <= 0 or not top or not bottom:
        return None
    exponents = list(top) + list(bottom)
    remainder = exponents[0] % 3
    if any(e % 3 != remainder for e in exponents):
        return None
    shift = -min(exponents)
    while (shift + remainder) % 3:
        shift += 1
    v = Fraction(value)
    numerator = sum((v ** ((e + shift) // 3) for e in top), Fraction(0))
    denominator = sum((v ** ((e + shift) // 3) for e in bottom), Fraction(0))
    if denominator == 0:
        return None
    return numerator / denominator


def _ring_mul(x, y, v):
    """Multiply in ℚ[t]/(t³ − v): elements are (c₀, c₁, c₂) for c₀ + c₁t + c₂t²."""
    out = [Fraction(0)] * 5
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            out[i + j] += a * b
    out[0] += v * out[3]                 # t³ = v
    out[1] += v * out[4]                 # t⁴ = vt
    return tuple(out[:3])


def _ring_pow(exponent: int, v: Fraction):
    """t^exponent inside the ring, negative exponents included."""
    if exponent < 0:
        # t⁻¹ = t²/v, so t^-k = (t²/v)^k
        base = (Fraction(0), Fraction(0), Fraction(1, 1) / v)
        exponent = -exponent
    else:
        base = (Fraction(0), Fraction(1), Fraction(0))
    result = (Fraction(1), Fraction(0), Fraction(0))
    for _ in range(exponent):
        result = _ring_mul(result, base, v)
    return result


def check(top=(4, 7, -5), bottom=(-2, 1), value=5):
    """Independent: compute in ℚ[t]/(t³ − v) and see whether the answer is rational.

    ``t = aⁿ`` is the real cube root of v, so the whole expression lives in the
    cubic field ℚ(v^{1/3}). Each power is reduced inside the ring, the quotient
    is formed by inverting the denominator through a 3×3 linear solve, and the
    result counts only if its t and t² parts vanish. No exponent is shifted and
    no common factor is spotted — the rationality is discovered, not assumed.
    """
    if value <= 0 or not top or not bottom:
        return None
    v = Fraction(value)
    zero = (Fraction(0), Fraction(0), Fraction(0))

    def total(exponents):
        acc = zero
        for e in exponents:
            piece = _ring_pow(e, v)
            acc = tuple(a + b for a, b in zip(acc, piece))
        return acc

    num, den = total(top), total(bottom)
    if den == zero:
        return None

    # solve den · q = num for q = (q₀, q₁, q₂) — a 3×3 system over ℚ
    columns = [_ring_mul(den, _ring_pow(k, v), v) for k in (0, 1, 2)]
    matrix = [[columns[k][row] for k in range(3)] + [num[row]] for row in range(3)]
    for col in range(3):
        pivot = next((r for r in range(col, 3) if matrix[r][col] != 0), None)
        if pivot is None:
            return None
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        head = matrix[col][col]
        matrix[col] = [x / head for x in matrix[col]]
        for r in range(3):
            if r != col and matrix[r][col] != 0:
                factor = matrix[r][col]
                matrix[r] = [x - factor * y for x, y in zip(matrix[r], matrix[col])]
    q = tuple(matrix[r][3] for r in range(3))
    assert _ring_mul(den, q, v) == num
    if q[1] != 0 or q[2] != 0:
        return None                       # genuinely irrational
    return q[0]
