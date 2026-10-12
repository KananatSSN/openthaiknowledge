"""Book chapters the catalog had no set for.

ป.2 เงิน and รูปเรขาคณิต; ม.2 การให้เหตุผลทางเรขาคณิต (isosceles triangles,
the exterior angle, converses); from the ม.4 additional book the function
chapter's inverse functions and graph shifts, and the graphs of exponential
and logarithmic functions; from ม.5 the law of sines with the ½ab sin C area,
the cross product, nth roots of a complex number, and present value with
loan instalments; from basic ม.6 grouped data — class boundaries and
midpoints, relative and cumulative frequency.

Registry levels follow the topics' existing sets (``ลอการิทึม`` is registered
at ม.5 and filed at ม.4, ``เวกเตอร์`` at ม.6 and filed at ม.5).
"""

from __future__ import annotations

from fractions import Fraction

from otk.kit.math_problems import frac_tex

P2 = {"th": "ป.2"}
M5 = {"th": "ม.5"}
M6 = {"th": "ม.6"}
NL = chr(10)


def _distinct(correct: str, *candidates: str) -> list[str]:
    """Candidates in the order given, minus repeats and the answer."""
    out: list[str] = []
    for c in candidates:
        if c != correct and c not in out:
            out.append(c)
    return out


def _deg(x) -> str:
    return rf"{x}^{{\circ}}"


# ── เงิน (ค 2.1 ป.2) ──────────────────────────────────────────────────────────


# ── รูปเรขาคณิต (ค 2.2 ป.2) ──────────────────────────────────────────────────


# ── การให้เหตุผลทางเรขาคณิต (ค 2.2 ม.2) ────────────────────────────────────────


# ── ฟังก์ชัน (ค 1.2 ม.4 เพิ่มเติม) ────────────────────────────────────────────


def _lin(a: int, b: int, var: str = "x") -> str:
    """3, -2 -> '3x - 2'; -1, 4 -> '-x + 4'; 1, 0 -> 'x'."""
    lead = var if a == 1 else f"-{var}" if a == -1 else f"{a}{var}"
    return lead if not b else f"{lead} + {b}" if b > 0 else f"{lead} - {-b}"


# ── กฎของไซน์ (ม.5 เพิ่มเติม) ─────────────────────────────────────────────────

# sin θ as q·√n for the angles the books use.
_SIN = {30: (Fraction(1, 2), 1), 45: (Fraction(1, 2), 2), 60: (Fraction(1, 2), 3), 90: (Fraction(1), 1),
        120: (Fraction(1, 2), 3), 135: (Fraction(1, 2), 2), 150: (Fraction(1, 2), 1)}


def _surd(q: Fraction, n: int) -> tuple[Fraction, int]:
    """q·√n with the square factors of n moved out."""
    out, f = 1, 2
    while f * f <= n:
        while n % (f * f) == 0:
            n //= f * f
            out *= f
        f += 1
    return Fraction(q) * out, n


def _mul(x, y):
    return _surd(x[0] * y[0], x[1] * y[1])


def _div(x, y):
    return _surd(x[0] / (y[0] * y[1]), x[1] * y[1])


def _surd_tex(x) -> str:
    q, n = _surd(*x)
    if n == 1:
        return frac_tex(q)
    root = rf"\sqrt{{{n}}}"
    if q.denominator == 1:
        return root if q == 1 else f"{q.numerator}{root}"
    num = "" if q.numerator == 1 else str(q.numerator)
    return rf"\frac{{{num}{root}}}{{{q.denominator}}}"


def _surd_bump(x) -> str:
    q, n = _surd(*x)
    return _surd_tex((q + 1, n))


# ── เวกเตอร์ และจำนวนเชิงซ้อน (ม.5 เพิ่มเติม) ───────────────────────────────────


# ── ลำดับและอนุกรม มูลค่าปัจจุบันและค่างวด (ค 1.2 ม.5 พื้นฐาน) ──────────────────────


# ── การนำเสนอข้อมูลเชิงปริมาณ (ค 3.1 ม.6 พื้นฐาน) ─────────────────────────────


