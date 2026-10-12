"""More ชุดโจทย์ for the number, arithmetic, fraction, measurement and
number-theory arms of the skill tree.

Same machinery as :mod:`otk.kit.math_problems` — these are extra types, split
into their own module only to keep that one navigable. Each carries the
``level``/``topic`` of a หัวข้อ the skill tree already claims, so it joins the
right concept node with no change to the tree itself.
"""

from __future__ import annotations


def _round10(n: int) -> int:
    """Round to the nearest ten, halves upward — what ป.4 is taught.

    Not ``round(n, -1)``: Python rounds halves to even, so ``round(45, -1)``
    is 40, and the generated answer would contradict the lesson.
    """
    return (n + 5) // 10 * 10


# ── จำนวน ────────────────────────────────────────────────────────────────────


# ── การคำนวณ ─────────────────────────────────────────────────────────────────


# ── เศษส่วนและทศนิยม ─────────────────────────────────────────────────────────


# ── การวัด ───────────────────────────────────────────────────────────────────


# ── ทฤษฎีจำนวน ───────────────────────────────────────────────────────────────


