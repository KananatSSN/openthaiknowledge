"""Harder application sets for the สสวท. เพิ่มเติม track (ม.4–ม.6).

The application stage of these topics was mostly one computation in one
wording. Each set here is an exam-style situation that takes two or more
steps — model it, compute, then answer the question actually asked (a time,
a difference, a cost, a range) — in five different situations.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

M4, M5, M6 = {"th": "ม.4"}, {"th": "ม.5"}, {"th": "ม.6"}


def _c(n: int) -> str:
    """12345 -> 12{,}345 (a thousands comma KaTeX does not space out)."""
    return f"{n:,}".replace(",", "{,}")


def _fr(f: Fraction) -> str:
    if f.denominator == 1:
        return _c(f.numerator)
    sign = "-" if f < 0 else ""
    return rf"{sign}\frac{{{abs(f.numerator)}}}{{{f.denominator}}}"


def _root(n: int) -> str:
    """√n simplified: 48 -> 4\\sqrt{3}."""
    out, rest = 1, n
    for p in range(2, isqrt(n) + 1):
        while rest % (p * p) == 0:
            out, rest = out * p, rest // (p * p)
    if rest == 1:
        return str(out)
    return (str(out) if out > 1 else "") + rf"\sqrt{{{rest}}}"


# ── ม.5 กฎของโคไซน์ ─────────────────────────────────────────────────────────────


# ── ม.5 อัตราส่วนตรีโกณมิติ: two angles of elevation ────────────────────────────


# ── ม.5 เวกเตอร์: resultants ─────────────────────────────────────────────────────


# ── ม.5 เมทริกซ์: two-unknown situations ─────────────────────────────────────────


# ── ม.5 ค่าคาดหมาย: is the game worth playing ─────────────────────────────────────


# ── ม.4 อสมการกำลังสอง: when is it at least … ─────────────────────────────────────


# ── ม.6 ลำดับเรขาคณิต: bounces, chains and savings ───────────────────────────────


# ── ม.6 ลำดับเลขคณิต: how many rows, which day ──────────────────────────────────


# ── ม.6 ค่าสูงสุด-ต่ำสุดสัมพัทธ์: optimisation ───────────────────────────────────


# ── ม.6 อินทิกรัลจำกัดเขต: accumulated change ────────────────────────────────────

