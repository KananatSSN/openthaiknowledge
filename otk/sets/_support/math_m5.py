"""ม.5 sets that the สสวท. books teach and the catalog did not have.

Basic track: ลำดับและอนุกรม with the money chapter — compound interest and
regular saving, the book's own reason for geometric series — and counting
beyond the single-formula drills: circular arrangements, identical items,
people who must sit together, handshakes and diagonals, probability by
counting. Additional track: angle-sum and double-angle formulas, the shape of
a sine graph, matrix inverses, 3×3 determinants, Cramer's rule, dot products,
and complex numbers in polar form.

Registry levels follow the topics' existing sets (``การเรียงสับเปลี่ยน``,
``การจัดหมู่``, ``ความน่าจะเป็น`` and ``เวกเตอร์`` are registered at ม.6 and
filed at ม.5).
"""

from __future__ import annotations

from decimal import Decimal

M5 = {"th": "ม.5"}
M6 = {"th": "ม.6"}


def money(v: Decimal) -> str:
    """12345.6 -> 12{,}345.60 (TeX)."""
    return f"{v:,.2f}".replace(",", "{,}")


# ── ลำดับและอนุกรม ดอกเบี้ย (ค 1.2 ม.5 พื้นฐาน) ──────────────────────────────────


# (rate %, years, (1 + r)^n to 6 dp) — the stem gives the factor, as the books do.
_FACTORS = ((2, 2, "1.0404"), (3, 2, "1.0609"), (4, 2, "1.0816"), (5, 2, "1.1025"),
            (2, 3, "1.061208"), (3, 3, "1.092727"), (4, 3, "1.124864"), (5, 3, "1.157625"),
            (10, 2, "1.21"), (10, 3, "1.331"), (6, 2, "1.1236"), (8, 2, "1.1664"))


def _base(r: int) -> str:
    """5 -> 1.05, 10 -> 1.1: one plus the rate, as the books write it."""
    return format(Decimal(100 + r) / 100, "f").rstrip("0")


# ── การนับ (ค 3.2 ม.5) ────────────────────────────────────────────────────────


# ── ตรีโกณมิติ (เพิ่มเติม ม.5) ────────────────────────────────────────────────


# ── เมทริกซ์ (เพิ่มเติม ม.5) ─────────────────────────────────────────────────

def _mat(m) -> str:
    rows = r" \\ ".join(" & ".join(str(x) for x in row) for row in m)
    return rf"\begin{{pmatrix}} {rows} \end{{pmatrix}}"


# ── เวกเตอร์ และจำนวนเชิงซ้อน (เพิ่มเติม ม.5) ─────────────────────────────────

def _vec(v) -> str:
    rows = r" \\ ".join(map(str, v))      # outside the f-string: Python 3.10 has no backslash there
    return rf"\begin{{bmatrix}} {rows} \end{{bmatrix}}"


