"""ข้อ 29 — ค่าของ XY² เมื่อ XY แบ่งบันไดหกจัตุรัสออกเป็นสองส่วนเท่ากัน

รูปสี่เหลี่ยมจัตุรัสมีด้านยาวด้านละ 2 หน่วย จำนวน 2 รูป ด้านละ 3 หน่วย จำนวน 2 รูป
ด้านละ 4 หน่วย จำนวน 1 รูป และรูปสี่เหลี่ยมจัตุรัสที่มีพื้นที่มากกว่า 4 ตารางหน่วย
จำนวน 1 รูป นำมาเรียงต่อกันดังรูป  ถ้าลากส่วนของเส้นตรงจากจุด X ไปยังจุด Y ทำให้แบ่ง
พื้นที่ออกเป็นสองส่วนเท่า ๆ กัน จงหาค่าของ XY²

**The layout is the data, and it has to be read off the crop.** Reading the
staircase left to right, with the origin at the bottom-left corner of the
3-square that carries the bottom edge:

    (0, 3) 3×3   the left square, X is its top-left corner
    (3, 3) 4×4   the tall one on top
    (2, 1) 2×2   the small one tucked under the left square
    (4, 0) 3×3   the bottom-middle square
    (7, 0) s×s   the unknown, **bottom-aligned** with the square to its left
    (7, −2) 2×2  the one hanging below, in a fixed position

So X = (0, 6) and Y = (7 + s, 0): only the unknown square's top edge and Y move
with s. Everything else stays put — which is the fact that makes the balance a
function of s alone.

**The halving condition has two roots.** Sweeping s, the area below XY equals
half the total at **s = 2 and again at s = 4**, an exact coincidence rather than
a near miss. That is what the printed "พื้นที่มากกว่า 4 ตารางหน่วย" is for: at
s = 2 the square's area is exactly 4, not more than 4, so only s = 4 survives.

    X = (0, 6), Y = (11, 0)   ⟹   XY² = 11² + 6² = **157**

Drop the inequality and the item has two answers; read it as ≥ and it still has
two. The strictness is load-bearing.

``solve`` works in exact fractions: the area of each square below the line has a
closed form (the integrand is a clamped linear function, so the interval splits
at the two crossings and each piece integrates exactly), and the roots are
bracketed, bisected, then snapped to rationals and **re-verified exactly**.
``check`` shares none of that: it measures the area below the line by summing a
fine grid of cells, sweeps s to bracket the sign changes of the same balance —
with the ``== 0`` case written first, since a root the grid lands on exactly is
the trap this repo has paid for three times — and measures XY² from the two
endpoints.
"""

from __future__ import annotations

from fractions import Fraction

#: everything scales with `scale`; `min_area` is the printed strict lower bound
#: on the unknown square's area, and it is what picks the root.
PARAMS = {"scale": 1, "min_area": 4}
ANSWER = 157
#: `check` measures the areas on a grid, so it lands a few parts in 10⁷ out.
TOL = 1e-6
VARIANTS = [
    {"scale": 2, "min_area": 16},
    {"scale": 2, "min_area": 20},
    {"scale": 3, "min_area": 36},
    {"scale": 1, "min_area": 5},
    {"scale": 4, "min_area": 64},
    {"scale": 1, "min_area": 1},        # both roots qualify: no single answer
]

#: (x, y, side) of the five fixed squares, before scaling. The sixth is the
#: unknown, at (7, 0) with side s.
FIXED = ((0, 3, 3), (3, 3, 4), (2, 1, 2), (4, 0, 3), (7, -2, 2))
UNKNOWN_AT = (7, 0)
X_CORNER = (0, 6)


def _below_in_square(square, xa, ya, xb, yb):
    """Exact area of the part of the square below the line through (xa,ya),(xb,yb).

    The height of the region over a vertical slice is ``clamp(line(x) − y0, 0,
    side)``, a linear function clamped twice, so the x-interval splits at the
    two crossings and each piece is a trapezoid.
    """
    x0, y0, side = (Fraction(v) for v in square)
    if xb == xa:
        return Fraction(0)
    slope = Fraction(yb - ya, xb - xa)
    intercept = Fraction(ya) - slope * Fraction(xa)

    def line(x):
        return slope * x + intercept

    cuts = {x0, x0 + side}
    if slope != 0:
        for level in (y0, y0 + side):
            x = (level - intercept) / slope
            if x0 < x < x0 + side:
                cuts.add(x)
    xs = sorted(cuts)

    total = Fraction(0)
    for left, right in zip(xs, xs[1:]):
        if right <= left:
            continue
        mid = (left + right) / 2
        # the piece is linear here, so the trapezoid rule is exact
        h_left = min(max(line(left) - y0, Fraction(0)), side)
        h_right = min(max(line(right) - y0, Fraction(0)), side)
        h_mid = min(max(line(mid) - y0, Fraction(0)), side)
        if h_left == h_right == h_mid:
            total += h_left * (right - left)
        else:
            total += (h_left + h_right) * (right - left) / 2
    return total


def _balance(s, scale):
    """area below XY − half the total, exactly. Zero is the halving condition."""
    s = Fraction(s)
    k = Fraction(scale)
    squares = [(x * k, y * k, side * k) for x, y, side in FIXED]
    squares.append((UNKNOWN_AT[0] * k, UNKNOWN_AT[1] * k, s))
    xa, ya = X_CORNER[0] * k, X_CORNER[1] * k
    xb, yb = UNKNOWN_AT[0] * k + s, Fraction(0)
    total = sum(side * side for _, _, side in squares)
    below = sum(_below_in_square(sq, xa, ya, xb, yb) for sq in squares)
    return below - total / 2


def _roots(scale, hi=12):
    """Every s > 0 where the line halves the area, as exact fractions."""
    k = Fraction(scale)
    grid = [Fraction(j, 8) * k for j in range(1, hi * 8 + 1)]
    found: list[Fraction] = []
    previous = None
    for s in grid:
        value = _balance(s, scale)
        if value == 0:                       # the grid landed on a root exactly
            if s not in found:
                found.append(s)
        elif previous is not None and previous[1] * value < 0:
            lo, hi_s = previous[0], s
            for _ in range(80):              # bisect, then snap and re-verify
                mid = (lo + hi_s) / 2
                if _balance(mid, scale) * _balance(lo, scale) <= 0:
                    hi_s = mid
                else:
                    lo = mid
            candidate = Fraction(float((lo + hi_s) / 2)).limit_denominator(64)
            if _balance(candidate, scale) == 0 and candidate not in found:
                found.append(candidate)
        previous = (s, value)
    return sorted(found)


def solve(scale=1, min_area=4):
    """XY² for the one root whose square is larger than the printed bound."""
    if scale <= 0 or min_area < 0:
        return None
    admissible = [s for s in _roots(scale) if s * s > min_area]
    if len(admissible) != 1:
        return None                          # ambiguous, or no such square
    s = admissible[0]
    k = Fraction(scale)
    dx = Fraction(UNKNOWN_AT[0]) * k + s - Fraction(X_CORNER[0]) * k
    dy = Fraction(X_CORNER[1]) * k
    value = dx * dx + dy * dy
    return int(value) if value.denominator == 1 else value


def check(scale=1, min_area=4, cells=1500):
    """Independent: measure the area below XY on a grid and sweep for the roots.

    Nothing is integrated in closed form and nothing is snapped to a fraction —
    each square is chopped into columns and the covered height per column is
    accumulated. The sweep tests ``== 0`` before it tests for a sign change,
    because a root the grid lands on exactly is otherwise missed.
    """
    if scale <= 0 or min_area < 0:
        return None
    k = float(scale)

    def below(s):
        squares = [(x * k, y * k, side * k) for x, y, side in FIXED]
        squares.append((UNKNOWN_AT[0] * k, UNKNOWN_AT[1] * k, s))
        xa, ya = X_CORNER[0] * k, X_CORNER[1] * k
        xb = UNKNOWN_AT[0] * k + s
        if xb == xa:
            return None
        slope = (0.0 - ya) / (xb - xa)
        total = 0.0
        for x0, y0, side in squares:
            step = side / cells
            for i in range(cells):
                x = x0 + (i + 0.5) * step
                height = slope * (x - xa) + ya - y0
                total += min(max(height, 0.0), side) * step
        return total

    def balance(s):
        area = below(s)
        fixed = sum(side * side * k * k for _, _, side in FIXED)
        return None if area is None else area - (fixed + s * s) / 2

    roots = []
    previous = None
    steps = 240
    for j in range(1, steps + 1):
        s = 12.0 * k * j / steps
        value = balance(s)
        if value is None:
            return None
        if abs(value) < 1e-9:
            roots.append(s)
        elif previous is not None and previous[1] * value < 0:
            lo, hi = previous[0], s
            for _ in range(60):
                mid = (lo + hi) / 2
                if balance(mid) * balance(lo) <= 0:
                    hi = mid
                else:
                    lo = mid
            roots.append((lo + hi) / 2)
        previous = (s, value)

    # The margin is the point of the printed inequality: the discarded root sits
    # exactly *on* the bound (s² = 4 when the bound is 4), and a grid-measured
    # root lands a few parts in 10⁶ away from it. Comparing to the bare bound
    # would keep or drop that root depending on which side the noise fell.
    margin = 1e-4 * max(1.0, min_area)
    admissible = [s for s in roots if s * s > min_area + margin]
    # a root the sweep found twice (once exactly, once by bracketing) is one root
    merged = []
    for s in sorted(admissible):
        if not merged or abs(s - merged[-1]) > 1e-6:
            merged.append(s)
    if len(merged) != 1:
        return None
    s = merged[0]
    dx = UNKNOWN_AT[0] * k + s - X_CORNER[0] * k
    dy = X_CORNER[1] * k
    value = dx * dx + dy * dy
    return round(value) if abs(value - round(value)) < 1e-6 else value
