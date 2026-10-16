"""Counting sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found four units, exercised by กสพท, A-level and O-NET
questions in ``openthaiknowledge-bank/rathcenter/12 หลักการนับ``, that no problem set
practised:

=====================================  ==========================================  ================
unit                                   set                                         topic
=====================================  ==========================================  ================
counting.complement                    math.counting_complement_m5                 หลักการนับ
counting.coloring                      math.coloring_regions_m5                    หลักการนับ
counting.adjacency                     math.arrangement_blocks_gaps_m5             การเรียงสับเปลี่ยน
counting.labelled-groups               math.distribute_to_groups_m5                การจัดหมู่
=====================================  ==========================================  ================

Every answer comes from a closed form; ``test_math_bank_counting.py``
recounts each one by brute-force enumeration and pins the source exams'
answers.
"""

from __future__ import annotations

from math import comb, factorial

from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion

M5 = {"th": "ม.5"}


def num(v: int) -> str:
    return f"{v:,}".replace(",", "{,}")


def _num_q(stem: list, right: int, named: list[int], topic: str) -> GeneratedQuestion:
    """Named mistakes first, then neighbours; non-positive and duplicate values dropped; three kept."""
    pool = [*named, right + 1, right - 1, right * 2, right + 2]
    wrongs = [num(w) for w in dict.fromkeys(pool) if w > 0 and w != right][:3]
    return GeneratedQuestion(stem=stem, correct=[content_math(num(right))],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


# ── Counting the complement ──────────────────────────────────────────────────


# ── Colouring regions ────────────────────────────────────────────────────────


def path_edges(n: int) -> tuple[tuple[int, int], ...]:
    return tuple((i, i + 1) for i in range(n - 1))


# ── Blocks, alternation, gaps ────────────────────────────────────────────────


# ── Distributing to named groups ─────────────────────────────────────────────


def one_extra_surjection(n: int) -> int:
    """n + 1 distinct people into n distinct rooms with no room empty: C(n + 1, 2)·n!."""
    return comb(n + 1, 2) * factorial(n)


