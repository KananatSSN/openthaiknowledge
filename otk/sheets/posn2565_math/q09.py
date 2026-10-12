"""ข้อ 9 — ค่าความจริงของ p, q และ p → q

ให้ ℝ เป็นเอกภพสัมพัทธ์  กำหนดให้
    p แทนประพจน์ ∀x∃y, x² − y = y² − x
    q แทนประพจน์ ∃x, 2x² + x + 2 = 0
จงหาค่าความจริงของประพจน์ p, ประพจน์ q และประพจน์ p → q ตามลำดับ

**p is true**, and cheaply: x² − y = y² − x rearranges to x² + x = y² + y, and
y = x satisfies it for every x. No discriminant needed — the existential is
witnessed by the x you were handed.

**q is false**: 2x² + x + 2 has discriminant 1 − 16 = −15 < 0, so it has no real
root.

Hence p → q is T → F = **false**, and the answer is (T, F, F). The implication is
the point: a true antecedent with a false consequent is the one case that fails,
and reading p as false (the usual slip) would make the implication true.

``PARAMS`` carries the quadratic's coefficients and the direction of the
implication, so the generator can flip q's truth value and ask q → p as well.
"""

from __future__ import annotations

#: q is ∃x, ax² + bx + c = 0; direction "pq" asks p → q, "qp" asks q → p.
PARAMS = {"a": 2, "b": 1, "c": 2, "direction": "pq"}
ANSWER = ("T", "F", "F")
VARIANTS = [
    {"a": 1, "b": -3, "c": 2},              # q true: roots 1 and 2
    {"a": 2, "b": 1, "c": 2, "direction": "qp"},
    {"a": 1, "b": -3, "c": 2, "direction": "qp"},
    {"a": 1, "b": 0, "c": 0},               # q true: the double root 0
    {"a": 0, "b": 0, "c": 5},               # not a quadratic at all
]


def solve(a=2, b=1, c=2, direction="pq"):
    """(p, q, implication) as T/F letters."""
    if a == 0 or direction not in ("pq", "qp"):
        return None
    p = True                                 # y = x always witnesses it
    q = b * b - 4 * a * c >= 0
    imp = (not p) or q if direction == "pq" else (not q) or p
    return tuple("T" if v else "F" for v in (p, q, imp))


def check(a=2, b=1, c=2, direction="pq"):
    """Independent: decide both propositions by searching, not by algebra.

    p is tested by taking many x and hunting for a y that works — over a grid and
    then by bisection on the quadratic in y — and q by scanning for a sign change
    in ax² + bx + c. Neither uses the rearrangement or the discriminant.
    """
    if a == 0 or direction not in ("pq", "qp"):
        return None

    def has_y(x: float) -> bool:
        """Some y with x² - y = y² - x, i.e. y² + y - x² - x = 0."""
        def f(y: float) -> float:
            return y * y + y - x * x - x
        lo, hi = -1000.0, 1000.0
        prev = f(lo)
        steps = 4000
        for i in range(1, steps + 1):
            cur = f(lo + (hi - lo) * i / steps)
            if cur == 0 or prev * cur < 0:
                return True
            prev = cur
        return False

    p = all(has_y(x) for x in (-9.5, -1.0, 0.0, 0.25, 3.0, 17.0))

    def g(x: float) -> float:
        return a * x * x + b * x + c

    q = False
    prev = g(-10000.0)
    for i in range(1, 200001):
        cur = g(-10000.0 + 20000.0 * i / 200000)
        if cur == 0 or prev * cur < 0:
            q = True
            break
        prev = cur
    if not q:                                # a double root touches without crossing
        vertex = -b / (2 * a)
        q = abs(g(vertex)) < 1e-12

    imp = (not p) or q if direction == "pq" else (not q) or p
    return tuple("T" if v else "F" for v in (p, q, imp))
