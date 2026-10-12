"""ข้อ 15 — ระยะห่างระหว่างจุด A และจุด B

ให้ A และ B เป็นจุดบนพาราโบลา y = 4x² + 7x − 1 ที่มีจุด (0, 0) เป็นจุดกึ่งกลาง
ระหว่างสองจุดนี้ จงหาระยะห่างระหว่างจุด A และจุด B

The origin being the midpoint means B = −A, so writing A = (u, v):

    v = au² + bu + c        (A on the parabola)
    −v = au² − bu + c       (B on the parabola)

Adding kills the odd part: ``2au² + 2c = 0``, so **u² = −c/a** — the quadratic
term and the constant decide the abscissa on their own. Subtracting gives
``v = bu``, so the point is (u, bu) and

    AB = 2√(u² + v²) = 2|u|√(1 + b²) = 2√(−c/a)·√(1 + b²)

For 4x² + 7x − 1: u² = 1/4, u = ±1/2, v = ±7/2, and

    AB = 2·½·√50 = √50 = **5√2** ≈ 7.0711

Such a pair exists only when ``c/a < 0``, i.e. when the origin is *inside* the
parabola's arms — otherwise no chord is bisected by it and ``solve`` returns None.

``solve`` uses the closed form. ``check`` looks for the pair numerically: it
sweeps u, measures how far ``(−u, −(au²+bu+c))`` misses the curve, bisects the
sign changes, and only then computes a distance.
"""

from __future__ import annotations

from math import sqrt

#: the parabola y = a·x² + b·x + c; the midpoint is the origin.
PARAMS = {"a": 4, "b": 7, "c": -1}
ANSWER = 7.0710678118654755
TOL = 1e-9
VARIANTS = [
    {"a": 1, "b": 0, "c": -4},
    {"a": 2, "b": 3, "c": -8},
    {"a": 1, "b": 5, "c": -1},
    {"a": 3, "b": -2, "c": -12},
    {"a": 4, "b": 7, "c": 1},          # same sign: the origin bisects no chord
    {"a": 0, "b": 7, "c": -1},         # not a parabola
]


def exact_square(a=4, b=7, c=-1):
    """AB² as a whole number when it is one, else None."""
    if a == 0:
        return None
    value = 4 * (1 + b * b) * (-c)
    if value <= 0 or value % a:
        return None
    return value // a


def solve(a=4, b=7, c=-1):
    """AB = 2√(−c/a)·√(1 + b²)."""
    if a == 0:
        return None
    ratio = -c / a
    if ratio <= 0:
        return None
    return 2 * sqrt(ratio) * sqrt(1 + b * b)


def check(a=4, b=7, c=-1):
    """Independent: hunt for the symmetric pair numerically and measure it.

    For each u the point (u, y(u)) is taken on the curve and its reflection
    (−u, −y(u)) is tested against the curve; the residual is swept, its sign
    changes are bisected, and each root found is verified on *both* points before
    the distance is taken. Nothing about the odd and even parts is used.
    """
    if a == 0:
        return None

    def y(x: float) -> float:
        return a * x * x + b * x + c

    def residual(u: float) -> float:
        """How far the reflection of (u, y(u)) misses the parabola."""
        return -y(u) - y(-u)

    lo, hi, steps = -200.0, 200.0, 200_000
    roots = []
    prev, prev_u = residual(lo), lo
    for i in range(1, steps + 1):
        u = lo + (hi - lo) * i / steps
        cur = residual(u)
        if cur == 0.0:
            # the sweep can land exactly on a root — u = ±1/2 here — and then
            # there is no sign change to bracket.
            roots.append(u)
        elif prev * cur < 0:
            left, right = prev_u, u
            for _ in range(200):
                mid = (left + right) / 2
                if residual(left) * residual(mid) <= 0:
                    right = mid
                else:
                    left = mid
            roots.append((left + right) / 2)
        prev, prev_u = cur, u

    distances = []
    for u in roots:
        if abs(u) < 1e-9:
            continue
        v = y(u)
        if abs(-v - y(-u)) > 1e-6:
            continue
        distances.append(2 * sqrt(u * u + v * v))
    if not distances:
        return None
    if max(distances) - min(distances) > 1e-6:
        return None
    return sum(distances) / len(distances)
