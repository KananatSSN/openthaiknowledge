"""ข้อ 5 — ถ้า AH = 2HD แล้ว D, S, T อยู่บนเส้นตรงเดียวกัน  (พิสูจน์)

With B = (0, 0), C = (1, 0) and A = (1, 3s)/(1 + 3s²), the orthocentre H satisfies
AH = 2HD, and S, T (the second meetings of the circumcircle with the circles on
diameters BH and CH) lie on one line through D, of slope (1 − 3s²)/(4s). The
solver returns that slope (s = 1/2: 1/8).

``check`` builds H, D, both diameter circles and the circumcircle, finds S and T
by reflecting B and C in the lines of centres, asserts AH = 2HD and that D, S, T
are collinear, and returns the slope of ST.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"s": Fraction(1, 2)}
ANSWER = Fraction(1, 8)
VARIANTS = [{"s": Fraction(1, 3)}, {"s": Fraction(2, 3)}, {"s": Fraction(1)}, {"s": Fraction(3, 2)}]


def solve(s=Fraction(1, 2)):
    return (1 - 3 * s * s) / (4 * s)


def _reflect(p, u, v):
    dx, dy = v[0] - u[0], v[1] - u[1]
    t = ((p[0] - u[0]) * dx + (p[1] - u[1]) * dy) / (dx * dx + dy * dy)
    return (2 * (u[0] + t * dx) - p[0], 2 * (u[1] + t * dy) - p[1])


def check(s=Fraction(1, 2)):
    A = (1 / (1 + 3 * s * s), 3 * s / (1 + 3 * s * s))
    B, C = (Fraction(0), Fraction(0)), (Fraction(1), Fraction(0))
    D = (A[0], Fraction(0))
    # orthocentre: on x = A_x, and BH ⊥ AC
    hy = A[0] * (C[0] - A[0]) / A[1]
    H = (A[0], hy)
    assert A[1] - H[1] == 2 * (H[1] - D[1])
    ox = Fraction(1, 2)
    oy = (A[0] ** 2 + A[1] ** 2 - A[0]) / (2 * A[1])
    centre = (ox, oy)
    S = _reflect(B, centre, ((B[0] + H[0]) / 2, (B[1] + H[1]) / 2))
    T = _reflect(C, centre, ((C[0] + H[0]) / 2, (C[1] + H[1]) / 2))
    assert (S[0] - D[0]) * (T[1] - D[1]) == (S[1] - D[1]) * (T[0] - D[0])
    return (T[1] - S[1]) / (T[0] - S[0])
