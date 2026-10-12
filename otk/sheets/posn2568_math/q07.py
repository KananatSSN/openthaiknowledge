"""ข้อ 7 — ระบบสมการที่ยุบเป็นทวินาม (x±y)⁵

จงหาคู่อันดับ (x, y) ของจำนวนจริงทั้งหมดที่สอดคล้องกับระบบสมการ
    A/(2x) + B/y = (3x² + y²)(x² + 3y²)          (โจทย์: A = B = 1)
    A/(2x) − B/y = 2(y⁴ − x⁴)

Method: add and subtract the two equations. The right-hand sides collapse into
the odd and even halves of a fifth power:
    add   →  A  = x⁵ + 10x³y² + 5xy⁴
    minus →  2B = 5x⁴y + 10x²y³ + y⁵
and those are exactly the two halves of the binomial expansion, so
    (x+y)⁵ = A + 2B      and      (x−y)⁵ = A − 2B.
Two real fifth roots later, x and y are half their sum and difference. For
A = B = 1 that is x = (⁵√3 − 1)/2, y = (⁵√3 + 1)/2.

``check`` is a two-variable Newton solve on the *original* system, started away
from the answer — it never uses the binomial identity.
"""

from __future__ import annotations

PARAMS = {"a": 1, "b": 1}
ANSWER = (0.1228654698077587, 1.1228654698077587)
# a == 2·b is excluded on purpose: there x − y = 0, the map (S, D) ↦ (S⁵, D⁵)
# has a singular Jacobian, and ``check``'s Newton stalls on the quintuple root.
# ``solve`` handles that case correctly (x = y = (A/2 · ½)^…); it just cannot be
# cross-checked this way, so the generator steers clear of it too.
VARIANTS = [
    {"a": 3, "b": 1},
    {"a": 1, "b": 3},
    {"a": 5, "b": 2},
    {"a": 32, "b": 1},
    {"a": 10, "b": 7},
]


def _fifth_root(v: float) -> float:
    """Real fifth root, sign included (Python's ** would go complex)."""
    return -((-v) ** 0.2) if v < 0 else v ** 0.2


def solve(a=1, b=1):
    """The unique real (x, y)."""
    s = _fifth_root(a + 2 * b)          # x + y
    d = _fifth_root(a - 2 * b)          # x − y
    return ((s + d) / 2, (s - d) / 2)


def residuals(x: float, y: float, a=1, b=1) -> tuple[float, float]:
    """How far (x, y) is from satisfying the system as literally written."""
    left = a / (2 * x)
    return (left + b / y - (3 * x * x + y * y) * (x * x + 3 * y * y),
            left - b / y - 2 * (y ** 4 - x ** 4))


def check(a=1, b=1, tol=1e-13):
    """Independent: Newton on the original two equations, numeric Jacobian."""
    x, y = 0.4, 1.7                     # deliberately not near the answer
    for _ in range(400):
        f1, f2 = residuals(x, y, a, b)
        h = 1e-7
        j11 = (residuals(x + h, y, a, b)[0] - f1) / h
        j12 = (residuals(x, y + h, a, b)[0] - f1) / h
        j21 = (residuals(x + h, y, a, b)[1] - f2) / h
        j22 = (residuals(x, y + h, a, b)[1] - f2) / h
        det = j11 * j22 - j12 * j21
        if abs(det) < 1e-18:
            raise ValueError("singular Jacobian")
        dx = (f1 * j22 - f2 * j12) / det
        dy = (j11 * f2 - j21 * f1) / det
        x, y = x - dx, y - dy
        if abs(dx) + abs(dy) < tol:
            break
    r1, r2 = residuals(x, y, a, b)
    if abs(r1) + abs(r2) > 1e-6:
        raise ValueError(f"Newton did not converge: residuals {r1:.3g}, {r2:.3g}")
    return (x, y)
