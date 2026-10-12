"""More ชุดโจทย์ for the geometry, trigonometry and coordinate-geometry arms.

Companion to :mod:`otk.sets._support.math_number`; see that module's docstring
for how these join the skill tree.

Geometry without a picture: every item here states its figure in words (the
prompt) and its measurements as notation, which is the same discipline the
existing ``math.pythagoras`` and ``math.similar_triangle`` types follow. Angles
and lengths are chosen so the answers stay exact — no rounded decimals.
"""

from __future__ import annotations

# Pythagorean triples, so right-triangle answers come out whole.
_TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29),
            (9, 40, 41), (6, 8, 10), (9, 12, 15)]

# Exact special-angle values, as TeX.
_SIN = {0: "0", 30: r"\frac{1}{2}", 45: r"\frac{\sqrt{2}}{2}",
        60: r"\frac{\sqrt{3}}{2}", 90: "1"}
_COS = {0: "1", 30: r"\frac{\sqrt{3}}{2}", 45: r"\frac{\sqrt{2}}{2}",
        60: r"\frac{1}{2}", 90: "0"}
_TAN = {0: "0", 30: r"\frac{\sqrt{3}}{3}", 45: "1", 60: r"\sqrt{3}"}


# ── เรขาคณิต: รูปสองมิติและสามมิติ ────────────────────────────────────────────

_POLYGONS = [("รูปสามเหลี่ยม", 3), ("รูปสี่เหลี่ยม", 4), ("รูปห้าเหลี่ยม", 5),
             ("รูปหกเหลี่ยม", 6), ("รูปเจ็ดเหลี่ยม", 7), ("รูปแปดเหลี่ยม", 8),
             ("รูปเก้าเหลี่ยม", 9), ("รูปสิบเหลี่ยม", 10)]


# ── ตรีโกณมิติ ───────────────────────────────────────────────────────────────


# ── เรขาคณิตวิเคราะห์ ────────────────────────────────────────────────────────


