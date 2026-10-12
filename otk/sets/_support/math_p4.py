"""ป.4 sets that the สสวท. books teach and the catalog did not have.

ป.4 had long multiplication and division drills, one decimal set and one
fraction-free week: no จำนวนนับที่มากกว่า 100,000, no เศษส่วน chapter
(proper, improper, mixed; adding with a denominator that is a multiple), no
decimal reading or arithmetic, no เวลา in days, weeks and years, and word
problems only as single sentences. This module adds them in book order.
"""

from __future__ import annotations

from fractions import Fraction

LEVEL = {"th": "ป.4"}


def grouped(n: int) -> str:
    """4572318 -> 4,572,318 (text)."""
    return f"{n:,}"


# ── จำนวนนับที่มากกว่า 100,000 (ค 1.1 ป.4) ───────────────────────────────────


# ── เศษส่วน (ค 1.1 ป.4) ──────────────────────────────────────────────────────


def fr(n: int, d: int) -> str:
    return rf"\frac{{{n}}}{{{d}}}"


def mixed(whole: int, n: int, d: int) -> str:
    return rf"{whole}\frac{{{n}}}{{{d}}}" if n else str(whole)


def as_mixed(value: Fraction) -> str:
    """An answer the ป.4 way: whole, proper fraction, or จำนวนคละ."""
    whole, rem = divmod(value.numerator, value.denominator)
    if not rem:
        return str(whole)
    return mixed(whole, rem, value.denominator) if whole else fr(rem, value.denominator)


def _not_equal(value: Fraction, texs: list[str], right: str) -> list[str]:
    """Wrong choices that are really wrong: none equal in value to the answer."""
    def val(t: str) -> Fraction:
        if r"\frac" not in t:
            return Fraction(int(t))
        head, rest = t.split(r"\frac{")
        n, d = rest.rstrip("}").split("}{")
        return int(head or 0) + Fraction(int(n), int(d))
    return [t for t in dict.fromkeys(texs) if t != right and val(t) != value and val(t) > 0]


# ── ทศนิยม (ค 1.1 ป.4) ───────────────────────────────────────────────────────


# ── โจทย์ปัญหาระคน (ค 1.1 ป.4) ───────────────────────────────────────────────


# ── เวลา (ค 2.1 ป.4) ─────────────────────────────────────────────────────────


# ── มุม (ค 2.2 ป.4) ─────────────────────────────────────────────────────────


# ── รูปสี่เหลี่ยมมุมฉาก (ค 2.1 ป.4) ──────────────────────────────────────────


# ── แผนภูมิแท่ง (ค 3.1 ป.4) ─────────────────────────────────────────────────


