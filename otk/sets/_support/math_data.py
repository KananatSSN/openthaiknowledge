"""More ชุดโจทย์ for the counting/probability, statistics and logic arms.

Companion to :mod:`otk.sets._support.math_number`; see that module's docstring
for how these join the skill tree.

Data sets are chosen so the statistics come out exact — means over a divisible
count, variances built from deviations that square to whole numbers — because a
rounded "answer" among rounded distractors is not a question with one answer.
"""

from __future__ import annotations


def _seq(nums) -> str:
    """A comma-separated number list as spacing-only TeX (no Thai)."""
    return r",\ ".join(str(n) for n in nums)


# ── การนับและความน่าจะเป็น ───────────────────────────────────────────────────


# ── สถิติ ────────────────────────────────────────────────────────────────────


# ── ตรรกศาสตร์และเซต ─────────────────────────────────────────────────────────


