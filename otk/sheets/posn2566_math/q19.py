"""ข้อ 19 — ค่ามากที่สุดของ p(1) เมื่อ p เป็นพหุนามกำลังสองที่สอดคล้องกับเงื่อนไข

กำหนดให้ p(x) = ax² + bx + c เป็นพหุนามกำลังสองที่สอดคล้องกับ
p(4) = p(−4) = 4, p(5) > 0 และ p(1) เป็นจำนวนเต็ม จงหาค่ามากที่สุดของ p(1)

p(4) = p(−4)  ⟹  the linear term vanishes at ±4 symmetrically, so
p is even: b = 0.  Then p(x) = ax² + c.

    p(4) = 16a + c = 4
    p(−4) = same, consistent
    c = 4 − 16a
    p(x) = a(x² − 16) + 4
    p(1) = a(1 − 16) + 4 = 4 − 15a
    p(5) = a(25 − 16) + 4 = 9a + 4 > 0  ⟹  a > −4/9

p(1) = 4 − 15a is maximised by minimising a. Since a > −4/9 and p(1) ∈ ℤ:
    −15a ∈ ℤ, so a = k/15 for some integer k.
    a > −4/9  ⟹  k/15 > −4/9  ⟹  k > −60/9 = −6.666…  ⟹  k ≥ −6.
    At k = −6: a = −6/15 = −2/5, p(1) = 4 − 15(−2/5) = 4 + 6 = **10**.

``solve`` computes directly.  ``check`` scans a over rationals with denominator
dividing 15 and finds the maximum p(1) that satisfies all constraints.
"""

from __future__ import annotations

from fractions import Fraction

#: p(val) = p(−val) = target, p(big) > 0, p(1) integer, maximise p(1).
PARAMS = {"val": 4, "target": 4, "big": 5}
ANSWER = 10
VARIANTS = [
    {"val": 3, "target": 3, "big": 4},
    {"val": 2, "target": 1, "big": 3},
    {"val": 5, "target": 5, "big": 6},
    {"val": 1, "target": 2, "big": 2},
    {"val": 4, "target": 4, "big": 10},
    {"val": 6, "target": 0, "big": 7},
]


def solve(val=4, target=4, big=5):
    """p(x) = a(x² − val²) + target; max p(1) s.t. a > −target/(big²−val²)."""
    if val == 0:
        return None         # then b ≠ 0 freely and p is not pinned
    v2 = val * val
    b2 = big * big
    if b2 == v2:
        return None         # p(big) constraint is vacuous
    # p(1) = a(1 − v2) + target = target + a(1 − v2)
    # p(big) = a(b2 − v2) + target > 0  →  a > −target/(b2 − v2) if b2 > v2
    coeff_1 = 1 - v2        # multiplied by a in p(1)
    coeff_b = b2 - v2       # multiplied by a in p(big)
    # a > −target/coeff_b
    if coeff_b > 0:
        a_lower = Fraction(-target, coeff_b)
    else:
        # a < −target/coeff_b  →  upper bound
        a_lower = None

    # p(1) = target + a * coeff_1 must be integer  →  a * coeff_1 ∈ ℤ
    # So a = k / |coeff_1| for integer k  (if coeff_1 ≠ 0)
    if coeff_1 == 0:
        return target  # p(1) = target always, just need a valid a

    denom = abs(coeff_1)

    if coeff_b > 0:
        # maximise p(1) = target − |coeff_1|·a  (coeff_1 < 0 when val > 1)
        # if coeff_1 < 0: p(1) = target + a·coeff_1, increasing a → decreasing p(1)
        # so minimise a; a > a_lower, a = k/denom
        # k > a_lower * denom
        k_lower_exact = a_lower * denom
        k_min = int(k_lower_exact) + 1
        # but check if k_lower_exact is exactly an integer (strict inequality)
        if Fraction(k_min - 1, 1) == k_lower_exact:
            pass  # k_min is already k_lower_exact + 1 effectively
        else:
            # k > k_lower_exact → k ≥ ceil(k_lower_exact + epsilon)
            import math
            k_min = math.ceil(float(k_lower_exact))
            if Fraction(k_min, 1) <= k_lower_exact:
                k_min += 1

        a_best = Fraction(k_min, denom)
    elif coeff_b < 0:
        # a < −target/coeff_b = target/|coeff_b|, so upper bound
        a_upper = Fraction(-target, coeff_b)
        # p(1) = target + a·coeff_1
        # if coeff_1 < 0: max p(1) → min a, no lower bound → −∞, not bounded
        # if coeff_1 > 0: max p(1) → max a, a < a_upper
        if coeff_1 > 0:
            k_upper_exact = a_upper * denom
            import math
            k_max = math.floor(float(k_upper_exact))
            if Fraction(k_max, 1) >= k_upper_exact:
                k_max -= 1
            a_best = Fraction(k_max, denom)
        else:
            return None  # unbounded
    else:
        return None

    result = target + a_best * coeff_1
    if result != int(result):
        return None
    return int(result)


def check(val=4, target=4, big=5):
    """Independent: scan a over rationals with small denominators."""
    if val == 0:
        return None
    v2 = val * val
    b2 = big * big
    if b2 == v2:
        return None
    coeff_1 = 1 - v2
    coeff_b = b2 - v2

    best = None
    # a = k/d for d in 1..v2, k in a generous range
    denom_range = abs(coeff_1) * abs(coeff_b) if abs(coeff_b) > 0 else abs(coeff_1)
    denom_range = max(denom_range, 100)
    for d in range(1, min(abs(coeff_1) + 1, 500) + 1):
        for k in range(-10 * d, 10 * d + 1):
            a = Fraction(k, d)
            # p(big) = a * coeff_b + target > 0
            pb = a * coeff_b + target
            if pb <= 0:
                continue
            # p(1) = a * coeff_1 + target must be integer
            p1 = a * coeff_1 + target
            if p1.denominator != 1:
                continue
            p1_int = int(p1)
            if best is None or p1_int > best:
                best = p1_int

    return best
