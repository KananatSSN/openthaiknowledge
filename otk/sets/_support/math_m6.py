"""ม.6 sets that the สสวท. books teach and the catalog did not have.

Basic track: the statistics chapter as it is used — the mean and median of a
frequency table, a weighted mean, the coefficient of variation to compare
spread, percentile rank, z-scores both ways, and prediction from a regression
line. Additional track: การแจกแจงความน่าจะเป็น (binomial and normal, which had
no set), optimisation and motion as applications of the derivative, and limits
of sequences.
"""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction

M6 = {"th": "ม.6"}


def _dec(v: Fraction, places: int = 2) -> str:
    """A fraction as a decimal, trailing zeros dropped: 13/4 -> 3.25."""
    d = (Decimal(v.numerator) / Decimal(v.denominator)).quantize(Decimal(1).scaleb(-places),
                                                                  rounding=ROUND_HALF_UP)
    s = format(d.normalize(), "f")
    return s


# ── ค่ากลางของข้อมูล (ค 3.1 ม.6 พื้นฐาน) ─────────────────────────────────────────


# ── การวัดการกระจาย ตำแหน่ง ค่ามาตรฐาน การถดถอย (ม.6 พื้นฐาน) ─────────────────


# ── การแจกแจงความน่าจะเป็น (เพิ่มเติม ม.6) ────────────────────────────────────


# ── แคลคูลัสประยุกต์ และลิมิตของลำดับ (เพิ่มเติม ม.6) ───────────────────────────


