"""Primary sets for indicators whose topic existed but no set taught them.

From an indicator-by-indicator check of the 2560 book against the catalog
after the content audit: two-step decimal problems at ป.4 (ค 1.1 ป.4/16);
dividing by a decimal and three-step decimal problems at ป.6 (ป.6/9–10);
writing a ratio from a situation (ป.6/2); ห.ร.ม. and ค.ร.น. of three numbers
(ป.6/4–5); writing a one-way table from raw data at ป.3 (ค 3.1 ป.3/2); and
naming angles and constructing one with a protractor at ป.4 (ค 2.2 ป.4/1,
ค 2.1 ป.4/2). In the additional course: adding, subtracting, multiplying and
dividing functions (จำนวนและพีชคณิต 2 ม.4/1); degree-3 and degree-4
polynomial equations and inequalities (3 ม.4/1, ม.5/6); and the transpose
and row operations (3 ม.5/3, 5).
"""

from __future__ import annotations

from decimal import Decimal
from random import Random


def _dec(value: Decimal, places: int) -> str:
    return f"{value:.{places}f}"


def _cents(rng: Random, lo: int, hi: int) -> Decimal:
    """A price in baht with satang that are multiples of 25."""
    return Decimal(rng.randint(lo, hi)) + Decimal(rng.choice((0, 25, 50, 75))) / 100


# ── ป.4 ทศนิยม (ค 1.1 ป.4/16) ─────────────────────────────────────────────────


# ── ป.6 ทศนิยม (ค 1.1 ป.6/9–10) ───────────────────────────────────────────────


# ── ป.6 อัตราส่วน (ค 1.1 ป.6/2) ───────────────────────────────────────────────


# ── ป.6 ห.ร.ม. และ ค.ร.น. ของสามจำนวน (ค 1.1 ป.6/4–5) ──────────────────────────


# ── ป.3 เขียนตารางทางเดียว (ค 3.1 ป.3/2) ──────────────────────────────────────


# ── ป.4 มุม (ค 2.2 ป.4/1, ค 2.1 ป.4/2) ────────────────────────────────────────


# ══ Additional course ════════════════════════════════════════════════════════

M4, M5 = {"th": "ม.4"}, {"th": "ม.5"}


# ── ม.4 การบวก ลบ คูณ หารฟังก์ชัน (จำนวนและพีชคณิต 2 ม.4/1) ──────────────────


def _nz(rng: Random, lo: int, hi: int) -> int:
    return rng.choice([n for n in range(lo, hi + 1) if n])


# ── ม.4 สมการและอสมการพหุนาม (จำนวนและพีชคณิต 3 ม.4/1, ม.5/6) ────────────────


# ── ม.5 เมทริกซ์สลับเปลี่ยน และการดำเนินการตามแถว (จำนวนและพีชคณิต 3 ม.5/3, 5) ─


