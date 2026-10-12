"""ป.5 sets that the สสวท. books teach and the catalog did not have.

ป.5 had fraction and decimal drills but no fraction word problems, no
multiplying or dividing decimals beyond powers of ten, no บัญญัติไตรยางศ์
(ค 1.1 ป.5), percentage problems of one sentence, and no ตารางสองทาง
(ค 3.1 ป.5). This module adds them in book order.
"""

from __future__ import annotations

from decimal import Decimal

LEVEL = {"th": "ป.5"}


def dstr(v: Decimal) -> str:
    """A decimal without trailing zeros, but never in exponent form."""
    s = format(v.normalize(), "f")
    return s


# ── โจทย์ปัญหาเศษส่วน (ค 1.1 ป.5) ────────────────────────────────────────────


# ── การคูณและการหารทศนิยม (ค 1.1 ป.5) ────────────────────────────────────────


# ── บัญญัติไตรยางศ์ (ค 1.1 ป.5) ──────────────────────────────────────────────


# ── โจทย์ปัญหาร้อยละ (ค 1.1 ป.5) ─────────────────────────────────────────────


# ── ปริมาตรและความจุ (ค 2.1 ป.5) ─────────────────────────────────────────────


# ── พื้นที่รูปสี่เหลี่ยม (ค 2.1 ป.5) ──────────────────────────────────────────


# ── ตารางสองทาง (ค 3.1 ป.5) ─────────────────────────────────────────────────


