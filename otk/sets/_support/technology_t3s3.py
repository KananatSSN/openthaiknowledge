"""Phase 7 Technology wave T3, slice 3 — reading drawn flowcharts, ม.1-ม.2.

The knowledge halves of ``ว 4.2 ม.1/1`` and ``ม.2/1``, which ask a learner to
design an algorithm and show it as a flowchart. Drawing one needs a diagram
editor the product does not have, so these sets *read* the charts drawn by
``flowcharts.py``; the Thai stem supplies the input value:

* ``ม.1/1`` — trace a straight chart, follow a decision (including the
  boundary value), and choose the statement that completes a chart.
* ``ม.2/1`` — count the passes of a loop, trace its output, and follow a loop
  that builds a total over ``i = 1`` to ``x``.
"""

from __future__ import annotations

from random import Random

from otk.sets._support import flowcharts as fc
from otk.sets._support.science_skills import diagram_question
from otk.sets._support.technology_t1s4 import _near

M1, M2 = {"th": "ม.1"}, {"th": "ม.2"}
FLIP = {"<": "<=", "<=": "<", ">": ">=", ">=": ">"}


def _ask(spec, *, stem: str, correct: str, wrongs, hint: str, topic: str):
    return diagram_question(spec.asset_id, fc.alt(spec), stem=stem, correct=correct,
                            wrongs=tuple(wrongs), hint=hint, topic=topic)


def _numbers(rng: Random, answer: int, slips) -> list[str]:
    return [str(w) for w in rng.sample(_near(answer, slips)[:5], 3)]


def _flipped(spec: fc.Flowchart) -> fc.Flowchart:
    """The same chart with ``<`` and ``<=`` (or ``>`` and ``>=``) swapped — the boundary slip."""
    left, sign, right = spec.test.split()
    return spec._replace(test=f"{left} {FLIP[sign]} {right}")


# ══ ว 4.2 ม.1/1 ═══════════════════════════════════════════════════════════════


# ══ ว 4.2 ม.2/1 ═══════════════════════════════════════════════════════════════


