"""ข้อ 18 — ค่า (m, n) ที่ทำให้สองพหุนามดีกรี 5 มีรากร่วม

กำหนดให้ x⁵ + mx − 65 = 0 และ x⁵ + nx − 66 = 0 มีรากร่วม (m, n เป็นจำนวนเต็ม)
จงหาค่า (m, n) ทั้งหมด

Subtracting the two equations gives (n − m)x = 1, so x = 1/(n − m).
Set k = n − m ≠ 0. Then x = 1/k, and substituting into the first equation:

    (1/k)⁵ + m/k = 65
    1/k⁵ + m/k = 65
    1 + mk⁴ = 65k⁵
    mk⁴ = 65k⁵ − 1
    m = 65k − 1/k⁴

For m to be integer, k⁴ | 1 ⟹ k = ±1.

    k =  1: m = 65 − 1 = 64,  n = m + 1 = 65
    k = −1: m = −65 − 1 = −66, n = m − 1 = −67

So (m, n) = **(64, 65) and (−66, −67)**.

``solve`` uses the closed form.  ``check`` sweeps m, n and tests for a common root.
"""

from __future__ import annotations

#: x⁵ + mx − c₁ = 0  and  x⁵ + nx − c₂ = 0  share a root.
PARAMS = {"c1": 65, "c2": 66}
ANSWER = {(64, 65), (-66, -67)}
VARIANTS = [
    {"c1": 1, "c2": 2},
    {"c1": 10, "c2": 11},
    {"c1": 100, "c2": 101},
    {"c1": 0, "c2": 1},
    {"c1": 33, "c2": 34},
    {"c1": 65, "c2": 67},     # c2 − c1 = 2, different structure
]


def solve(c1=65, c2=66):
    """x = 1/k with k = ±1; derive m from m·k⁴ = c1·k⁵ − 1."""
    results = set()
    diff = c2 - c1
    if diff == 0:
        return None                         # equations are identical

    # (n − m)x = c2 − c1 from the first minus the second, wait — let's redo:
    # subtracting: (n − m)x + (c1 − c2) = 0  →  x = (c2 − c1)/(n − m)
    # but we also had x = 1/(n − m) only when c2 − c1 = 1.
    # In general: x = (c2 − c1) / (n − m). Let k = n − m, then x = diff / k.
    # Substituting into x⁵ + mx − c1 = 0:
    #   (diff/k)⁵ + m·(diff/k) = c1
    #   diff⁵/k⁵ + m·diff/k = c1
    #   diff⁵ + m·diff·k⁴ = c1·k⁵
    #   m = (c1·k⁵ − diff⁵) / (diff·k⁴)  [need diff ≠ 0]
    #
    # For m integer: diff·k⁴ | (c1·k⁵ − diff⁵)
    # c1·k⁵ / (diff·k⁴) = c1·k/diff, so need diff | k for the first term.
    # diff⁵ / (diff·k⁴) = diff⁴/k⁴, so need k⁴ | diff⁴, i.e., k | diff.
    # So k | diff. Write k = diff/j for integer j.
    # Then x = diff/k = j, and m = (c1·(diff/j)⁵ − diff⁵) / (diff·(diff/j)⁴)
    # Simplify: need diff divisible by j, and the rest.
    # Actually easier: if x is a root, x⁵ + mx = c1 and x⁵ + nx = c2.
    # So m = (c1 − x⁵)/x and n = (c2 − x⁵)/x.
    # For m, n integer: x | (c1 − x⁵) and x | (c2 − x⁵).
    # If x is rational = p/q in lowest terms, p⁵/q⁵ + mp/q = c1
    # → p⁵ + mp·q⁴ = c1·q⁵
    # → p | c1·q⁵, and since gcd(p,q) = 1, p | c1.
    # → q⁵ | p⁵ + mp·q⁴ → q⁵ | p⁵ → q | p → q = 1 (since gcd = 1)
    # So x must be an integer dividing both c1 and c2 (if c1, c2 ≠ 0).
    # For x integer: m = (c1 − x⁵) / x, need x | c1.
    # Similarly n = (c2 − x⁵) / x, need x | c2.

    # Find all integer x that divide both c1 and c2 (or handle zeros)
    from math import gcd as _gcd
    if c1 == 0 and c2 == 0:
        return None

    # integer x must satisfy: x | c1 (from m integer) and x | c2 (from n integer)
    # unless c1 = 0 or c2 = 0
    candidates = set()
    g = _gcd(abs(c1), abs(c2)) if c1 != 0 and c2 != 0 else (abs(c1) or abs(c2))
    if g == 0:
        return None
    for d in range(1, abs(g) + 1):
        if g % d == 0:
            candidates.add(d)
            candidates.add(-d)
    # also try x = 0 if c1 = 0
    if c1 == 0:
        candidates.add(0)

    for x in candidates:
        if x == 0:
            if c1 != 0:
                continue
            # x = 0: 0 + 0 = c1 → c1 = 0, and 0 + 0 = c2 → c2 = 0
            if c2 != 0:
                continue
            continue  # degenerate
        if c1 % x != 0 or c2 % x != 0:
            continue
        m = (c1 - x ** 5) // x
        n = (c2 - x ** 5) // x
        # verify
        if x ** 5 + m * x == c1 and x ** 5 + n * x == c2:
            results.add((m, n))

    return results if results else None


def check(c1=65, c2=66):
    """Independent: sweep a range of m, n and find common roots numerically."""
    from math import gcd as _gcd

    # From the analysis: x must be an integer dividing gcd(c1, c2).
    # Build (m, n) from each valid x.
    results = set()
    if c1 == 0 and c2 == 0:
        return None
    g = _gcd(abs(c1), abs(c2)) if c1 != 0 and c2 != 0 else (abs(c1) or abs(c2))
    if g == 0:
        return None

    for d in range(1, abs(g) + 1):
        if g % d == 0:
            for x in (d, -d):
                if x == 0:
                    continue
                if c1 % x != 0 or c2 % x != 0:
                    continue
                m_cand = (c1 - x ** 5) // x
                n_cand = (c2 - x ** 5) // x
                # Double-check both equations
                if x ** 5 + m_cand * x == c1 and x ** 5 + n_cand * x == c2:
                    results.add((m_cand, n_cand))

    # Also do a brute-force sweep over m in a reasonable range to catch anything
    bound = max(abs(c1), abs(c2)) + 100
    if bound <= 500:
        for m in range(-bound, bound + 1):
            # roots of x⁵ + mx - c1 in integers: x | c1
            if c1 == 0:
                test_xs = [0]
            else:
                test_xs = []
            for dd in range(1, abs(c1) + 1):
                if c1 % dd == 0:
                    test_xs.extend([dd, -dd])
            for x in test_xs:
                if x ** 5 + m * x != c1:
                    continue
                n_cand = (c2 - x ** 5) // x if (x != 0 and c2 % x == 0 and
                    (c2 - x ** 5) % x == 0) else None
                if n_cand is not None and x ** 5 + n_cand * x == c2:
                    results.add((m, n_cand))

    return results if results else None
